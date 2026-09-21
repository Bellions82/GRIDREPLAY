from __future__ import annotations

from backend.core.config import settings
from backend.core.state import RenderState
from backend.database.models import GenerationRecord, QAResult, RenderJob
from backend.database.session import SessionLocal
from backend.director.motion import MotionPlanner
from backend.director.prompt_compiler import PromptCompiler
from backend.director.strategy import GenerationStrategy, ProviderCapability
from backend.qa.engine import QAEngine
from backend.rendering.generation_record import build_generation_record
from backend.rendering.provider import NullVideoProvider
from backend.workers.lease import claim_job, heartbeat
from backend.workers.redis_queue import RedisQueue

class RenderWorker:
    def __init__(self, worker_id: str, provider=None, capability: ProviderCapability | None = None):
        self.worker_id = worker_id
        self.provider = provider or NullVideoProvider()
        self.capability = capability or ProviderCapability(
            provider="null", model="provider-neutral", model_version="development",
            text_to_video=True
        )
        self.strategy = GenerationStrategy()
        self.motion = MotionPlanner()
        self.compiler = PromptCompiler()
        self.qa = QAEngine()

    async def process_once(self) -> bool:
        queue = RedisQueue(settings.redis_url)
        item = await queue.dequeue(timeout=1)
        if not item:
            await queue.close()
            return False

        job_id = item["job_id"]
        payload = item.get("payload", {})
        final_state = RenderState.FAILED
        requeue_payload = None

        async with SessionLocal() as session:
            if not await claim_job(session, job_id, self.worker_id):
                await session.commit()
                await queue.close()
                return True

            job = await session.get(RenderJob, job_id)
            if not job:
                await session.commit()
                await queue.close()
                return True

            job.state = RenderState.PROCESSING
            job.attempts += 1
            attempt = job.attempts
            payload = job.payload or payload
            await session.commit()

            try:
                shot = payload.get("shot", payload)
                strategy = self.strategy.select(shot, self.capability)
                motion = self.motion.plan(shot)
                compiled = self.compiler.compile(
                    canon=payload.get("canon", {}),
                    scene=payload.get("scene", {}),
                    shot=shot,
                    motion=motion,
                    composition=payload.get("composition", {}),
                )
                await heartbeat(session, job_id, self.worker_id)
                await session.commit()

                result = await self.provider.generate({
                    **compiled["provider_payload"],
                    "references": payload.get("references", []),
                    "parameters": payload.get("params", {}),
                    "duration": shot.get("duration", 0.0),
                    "generation_strategy": strategy,
                })

                record_data = build_generation_record(
                    shot_id=job.shot_id,
                    version=attempt,
                    provider=result.get("provider", self.capability.provider),
                    model=payload.get("model", self.capability.model),
                    model_version=result.get("model_version", self.capability.model_version),
                    prompt=compiled["prompt"],
                    negative_prompt=compiled["negative_prompt"],
                    seed=payload.get("seed"),
                    parameters={**payload.get("params", {}), "generation_strategy": strategy},
                    references=payload.get("references", []),
                )

                qa = await self.qa.evaluate_async({**result, "generation_record": record_data, "shot": shot}, shot=shot)
                record = GenerationRecord(
                    project_id=job.project_id, shot_id=job.shot_id, job_id=job.id,
                    version=attempt, provider=record_data["provider"], model=record_data["model"],
                    model_version=record_data["model_version"], prompt=record_data["prompt"],
                    negative_prompt=record_data["negative_prompt"], seed=record_data["seed"],
                    parameters=record_data["parameters"], references=record_data["references"],
                    artifact_uri=result.get("artifact_uri"), artifact_metadata=result, qc_result=qa,
                )
                session.add(record)
                await session.flush()

                session.add(QAResult(
                    project_id=job.project_id, shot_id=job.shot_id, job_id=job.id,
                    generation_id=record.id, attempt=attempt,
                    technical=qa["technical"], visual=qa["visual"], character=qa["character"],
                    environment=qa["environment"], temporal=qa["temporal"], timeline=qa["timeline"],
                    decision=qa["decision"], failure_codes=qa["failure_codes"],
                    repair_plan=qa["repair_plan"], metrics=qa["metrics"],
                ))

                if qa["decision"] == "APPROVED":
                    final_state = RenderState.APPROVED
                elif attempt >= settings.max_render_attempts:
                    final_state = RenderState.FAILED
                    job.last_error = f"max attempts reached: {qa['failure_codes']}"
                else:
                    final_state = RenderState.REGENERATE
                    requeue_payload = {
                        **payload,
                        "repair": qa["repair_plan"],
                        "previous_generation_version": attempt,
                    }

                job.state = final_state
                job.lease_owner = None
                job.lease_expires_at = None
                job.heartbeat_at = None
                if final_state == RenderState.APPROVED:
                    job.last_error = None
                await session.commit()

            except Exception as exc:
                job.last_error = str(exc)
                job.lease_owner = None
                job.lease_expires_at = None
                job.heartbeat_at = None
                if attempt >= settings.max_render_attempts:
                    final_state = RenderState.FAILED
                    job.state = final_state
                    await session.commit()
                else:
                    final_state = RenderState.REGENERATE
                    job.state = final_state
                    requeue_payload = payload
                    await session.commit()

        if final_state == RenderState.REGENERATE:
            await queue.enqueue(job_id, requeue_payload or payload)
        elif final_state == RenderState.FAILED:
            await queue.dead_letter_job(job_id, payload, "render/qa failure")
        await queue.close()
        return True
