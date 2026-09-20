from __future__ import annotations

import json
from typing import Any

from redis.asyncio import Redis

class RedisQueue:
    def __init__(self, url: str, queue_name: str = "videoforge:render") -> None:
        self.redis = Redis.from_url(url, decode_responses=True)
        self.queue_name = queue_name
        self.dead_letter = f"{queue_name}:dead"

    async def enqueue(self, job_id: str, payload: dict[str, Any]) -> None:
        await self.redis.rpush(self.queue_name, json.dumps({"job_id": job_id, "payload": payload}))

    async def dequeue(self, timeout: int = 5) -> dict[str, Any] | None:
        item = await self.redis.blpop(self.queue_name, timeout=timeout)
        if not item:
            return None
        return json.loads(item[1])

    async def dead_letter_job(self, job_id: str, payload: dict[str, Any], reason: str) -> None:
        await self.redis.rpush(self.dead_letter, json.dumps({"job_id": job_id, "payload": payload, "reason": reason}))

    async def ping(self) -> bool:
        return bool(await self.redis.ping())

    async def close(self) -> None:
        await self.redis.aclose()
