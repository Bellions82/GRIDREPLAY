import pytest
from backend.workers.renderer_worker import RenderWorker

class Provider:
    async def generate(self, request):
        assert "prompt" in request
        return {"provider": "test", "model_version": "1", "status": "OK"}

@pytest.mark.asyncio
async def test_worker_provider_contract():
    worker = RenderWorker("test", Provider())
    assert worker.provider is not None
