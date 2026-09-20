from __future__ import annotations

from sqlalchemy import select, update
from backend.core.state import RenderState
from backend.database.models import RenderJob
from backend.database.session import SessionLocal
from backend.director.motion import MotionPlanner
from backend.director.prompt_compiler import PromptCompiler
from backend.qa.engine import QAEngine
from backend.rendering.generation_record import build_generation_record
from backend.rendering.provider import NullVideoProvider
from backend.workers.lease import claim_job, heartbeat
from backend.workers.redis_queue import RedisQueue
from backend.core.config import settings

class RenderWorker:
    def __init__(self, worker_id: str, provider=None):
        self.worker_id = worker_id
        self.provider = provider or NullVideoProvider()
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
        async with SessionLocal() as session:
            if not await claim_job(session, job_id, self.worker_id):
                await session.commit()
                await queue.close()
                return True
            await session.commit()
            job = await session.get(RenderJob, job_id)
            if not job:
                await queue.close()
                return True
            payload = job.payload
            await session.execute(update(RenderJob).where(RenderJob.id == job_id).values(state=RenderState.PROCESSING, attempts=RenderJob.attempts + 1))
            await session.commit()
            shot = payload.get("shot", payload)
            motion = self.motion.plan(shot)
            compiled = self.compiler.compile(canon=payload.get("canon", {}), scene=payload.get("scene", {}), shot=shot, motion=motion, composition=payload.get("composition", {}))
            await heartbeat(session, job_id, self.worker_id)
            await session.commit()
            result = await self.provider.generate({**compiled["provider_payload"], "references": payload.get("references", []), "parameters": payload.get("params", {})})
            record = build_generation_record(shot_id=job.shot_id, version=job.attempts, provider=result.get("provider", "unknown"), model=payload.get("model", "provider-neutral"), model_version=result.get("model_version", ""), prompt=compiled["prompt"], negative_prompt=compiled["negative_prompt"], seed=payload.get("seed"), parameters=payload.get("params", {}), references=payload.get("references", []))
            qa = self.qa.evaluate({**result, "generation_record": record, "shot": shot})
            final_state = RenderState.APPROVED if qa["decision"] == "APPROVED" else RenderState.REGENERATE
            await session.execute(update(RenderJob).where(RenderJob.id == job_id).values(state=final_state, lease_owner=None, lease_expires_at=None, heartbeat_at=None, last_error=None if final_state == RenderState.APPROVED else str(qa)))
            await session.commit()
        if final_state == RenderState.REGENERATE:
            await queue.enqueue(job_id, payload)
        await queue.close()
        return True
