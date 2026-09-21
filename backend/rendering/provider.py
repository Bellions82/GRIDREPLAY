from typing import Protocol

class VideoProvider(Protocol):
    async def generate(self, request: dict) -> dict: ...

class NullVideoProvider:
    """Development provider; never represents production generation quality."""
    async def generate(self, request: dict) -> dict:
        return {
            "provider": "null",
            "model_version": "development",
            "artifact_uri": None,
            "artifact_status": "SIMULATED",
            "media_type": "video/mp4",
            "duration": float(request.get("duration", 0.0)),
            "status": "SIMULATED",
        }
