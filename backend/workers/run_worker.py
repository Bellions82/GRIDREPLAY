import asyncio
import os
from backend.workers.renderer_worker import RenderWorker

async def main() -> None:
    worker = RenderWorker(os.getenv("WORKER_ID", "render-worker-1"))
    while True:
        await worker.process_once()
        await asyncio.sleep(0.25)

if __name__ == "__main__":
    asyncio.run(main())
