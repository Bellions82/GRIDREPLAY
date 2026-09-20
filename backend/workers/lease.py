from __future__ import annotations

from datetime import datetime, timedelta, timezone
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.models import RenderJob

LEASE_SECONDS = 120

def utcnow() -> datetime:
    return datetime.now(timezone.utc)

async def claim_job(session: AsyncSession, job_id: str, worker_id: str) -> bool:
    now = utcnow()
    result = await session.execute(
        update(RenderJob)
        .where(RenderJob.id == job_id, RenderJob.lease_expires_at.is_(None))
        .values(lease_owner=worker_id, lease_expires_at=now + timedelta(seconds=LEASE_SECONDS), heartbeat_at=now, state="CLAIMED")
    )
    return result.rowcount == 1

async def heartbeat(session: AsyncSession, job_id: str, worker_id: str) -> bool:
    now = utcnow()
    result = await session.execute(
        update(RenderJob)
        .where(RenderJob.id == job_id, RenderJob.lease_owner == worker_id)
        .values(lease_expires_at=now + timedelta(seconds=LEASE_SECONDS), heartbeat_at=now)
    )
    return result.rowcount == 1
