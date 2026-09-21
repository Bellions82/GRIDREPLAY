from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class InspectionFrame:
    timestamp: float
    uri: str

class VisualInspector:
    """Provider-neutral inspection contract.

    Production adapters can attach CV/vision models without changing QA orchestration.
    """

    async def inspect(self, artifact: dict, *, references: list[str] | None = None) -> dict:
        supplied = artifact.get("inspection", {})
        return {
            "identity_similarity": supplied.get("identity_similarity"),
            "temporal_stability": supplied.get("temporal_stability"),
            "composition_score": supplied.get("composition_score"),
            "anatomy_score": supplied.get("anatomy_score"),
            "environment_similarity": supplied.get("environment_similarity"),
            "frame_count_checked": supplied.get("frame_count_checked", 0),
            "source": supplied.get("source", "not_configured"),
        }
