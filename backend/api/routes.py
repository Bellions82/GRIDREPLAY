from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from backend.core.fingerprint import render_fingerprint
from backend.core.state import RenderState
from backend.database.models import Project, RenderJob, Scene, Shot
from backend.database.session import session_scope
from backend.workers.redis_queue import RedisQueue
from backend.core.config import settings

router = APIRouter()

class ProjectRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    schema_version: str = "4.2"

class JobRequest(BaseModel):
    project_id: str
    scene_id: str
    shot_id: str | None = None
    asset_versions: list[str] = Field(default_factory=list)
    model: str = "provider-neutral"
    params: dict = Field(default_factory=dict)
    prompt: str = ""
    seed: int | None = None

@router.post("/projects")
async def create_project(req: ProjectRequest):
    async with session_scope() as session:
        project = Project(title=req.title, schema_version=req.schema_version)
        session.add(project)
        await session.flush()
        return {"project_id": project.id, "title": project.title, "status": project.status}

@router.post("/render-jobs")
async def create_render_job(req: JobRequest):
    payload = req.model_dump()
    fp = render_fingerprint(payload)
    created = False
    async with session_scope() as session:
        existing = await session.scalar(select(RenderJob).where(RenderJob.fingerprint == fp))
        if existing:
            return {"job_id": existing.id, "state": existing.state, "fingerprint": fp, "idempotent": True}
        project = await session.get(Project, req.project_id)
        scene = await session.get(Scene, req.scene_id)
        if not project or not scene or scene.project_id != req.project_id:
            raise HTTPException(status_code=404, detail="project or scene not found")
        shot = await session.get(Shot, req.shot_id) if req.shot_id else None
        if req.shot_id and (not shot or shot.scene_id != req.scene_id):
            raise HTTPException(status_code=404, detail="shot not found")
        if shot is None:
            shot = Shot(scene_id=req.scene_id, ordinal=0, duration=0.0, data={})
            session.add(shot)
            await session.flush()
        job = RenderJob(project_id=req.project_id, shot_id=shot.id, fingerprint=fp, state=RenderState.CREATED, payload=payload)
        session.add(job)
        await session.flush()
        job_id = job.id
        created = True
    if created:
        queue = RedisQueue(settings.redis_url)
        try:
            await queue.enqueue(job_id, payload)
        finally:
            await queue.close()
    return {"job_id": job_id, "state": RenderState.CREATED, "fingerprint": fp, "idempotent": False}
