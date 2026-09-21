from __future__ import annotations

class TechnicalInspector:
    """Provider-neutral media integrity contract; ffprobe/decoder adapter plugs in later."""

    async def inspect(self, artifact: dict) -> dict:
        supplied = artifact.get("technical", {})
        return {
            "playable": supplied.get("playable"),
            "duration": supplied.get("duration", artifact.get("duration")),
            "fps": supplied.get("fps"),
            "width": supplied.get("width"),
            "height": supplied.get("height"),
            "audio_present": supplied.get("audio_present"),
            "av_sync_ms": supplied.get("av_sync_ms"),
            "checksum": supplied.get("checksum"),
            "source": supplied.get("source", "not_configured"),
        }
