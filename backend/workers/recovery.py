from __future__ import annotations
from datetime import datetime, timezone
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.models import RenderJob

async def recover_expired_leases(session: AsyncSession, max_attempts: int = 3) -> list[str]:
    now = datetime.now(timezone.utc)
    result = await session.execute(select(RenderJob).where(RenderJob.lease_expires_at.is_not(None), RenderJob.lease_expires_at < now, RenderJob.state.in_(["CLAIMED", "PROCESSING"])))
    jobs = list(result.scalars())
    recovered = []
    for job in jobs:
        job.lease_owner = None
        job.lease_expires_at = None
        job.heartbeat_at = None
        job.attempts += 1
        if job.attempts >= max_attempts:
            job.state = "FAILED"
            job.last_error = "lease expired; retry limit reached"
        else:
            job.state = "QUEUED"
            recovered.append(job.id)
    return recovered
