from __future__ import annotations

from datetime import datetime, timezone

def build_generation_record(*, shot_id: str, version: int, provider: str, model: str,
                            model_version: str = "", prompt: str = "",
                            negative_prompt: str = "", seed: int | None = None,
                            parameters: dict | None = None, references: list[str] | None = None,
                            qc_result: dict | None = None) -> dict:
    return {
        "schema_version": "4.2",
        "shot_id": shot_id,
        "version": version,
        "provider": provider,
        "model": model,
        "model_version": model_version,
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "seed": seed,
        "parameters": parameters or {},
        "references": references or [],
        "qc_result": qc_result,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
