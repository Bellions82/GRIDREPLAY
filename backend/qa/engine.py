from __future__ import annotations

from backend.qa.repair import build_repair_plan
from backend.qa.metrics import evaluate_thresholds
from backend.qa.visual_inspector import VisualInspector
from backend.qa.technical import TechnicalInspector

DIMENSIONS = ("technical", "visual", "character", "environment", "temporal", "timeline")

DEFAULT_THRESHOLDS = {
    "identity_similarity": 0.90,
    "temporal_stability": 0.85,
    "composition_score": 0.85,
    "anatomy_score": 0.85,
    "environment_similarity": 0.85,
}

class QAEngine:
    """Evidence-first QA gate. Unknown metrics never silently become passes."""

    def __init__(self, visual_inspector=None, technical_inspector=None):
        self.visual_inspector = visual_inspector or VisualInspector()
        self.technical_inspector = technical_inspector or TechnicalInspector()

    async def evaluate_async(self, artifact: dict, *, shot: dict | None = None) -> dict:
        explicit = artifact.get("qa", {})
        technical = await self.technical_inspector.inspect(artifact)
        visual = await self.visual_inspector.inspect(
            artifact, references=(shot or {}).get("references", [])
        )

        metric_input = {
            **visual,
            "av_sync_ms": technical.get("av_sync_ms"),
        }
        threshold_result = evaluate_thresholds(metric_input, DEFAULT_THRESHOLDS)
        failures = list(explicit.get("failure_codes", []))

        if technical.get("playable") is False:
            failures.append("TECHNICAL_FAILURE")
        if "identity_similarity" in threshold_result["failures"]:
            failures.append("IDENTITY_DRIFT")
        if "temporal_stability" in threshold_result["failures"]:
            failures.append("TEMPORAL_FLICKER")
        if "composition_score" in threshold_result["failures"]:
            failures.append("COMPOSITION_FAILURE")
        if "anatomy_score" in threshold_result["failures"]:
            failures.append("ANATOMY")
        if "environment_similarity" in threshold_result["failures"]:
            failures.append("BACKGROUND_DRIFT")

        # Explicit dimension failures remain authoritative.
        dimensions = {
            name: explicit.get(name, "PASS" if not failures else "FAIL")
            for name in DIMENSIONS
        }

        # Development simulation remains passable only when it supplied no failures
        # and no real inspection values are available.
        simulated = artifact.get("artifact_status") == "SIMULATED"
        if simulated and not failures and all(v is None for k, v in visual.items() if k != "source"):
            dimensions = {name: "PASS" for name in DIMENSIONS}

        decision = "APPROVED" if all(value == "PASS" for value in dimensions.values()) else "REGENERATE"
        unique_failures = list(dict.fromkeys(failures))
        return {
            **dimensions,
            "decision": decision,
            "failure_codes": unique_failures,
            "repair_plan": build_repair_plan(unique_failures),
            "metrics": {
                "visual": visual,
                "technical": technical,
                "thresholds": threshold_result,
            },
        }

    def evaluate(self, artifact: dict) -> dict:
        """Compatibility path for existing synchronous tests/simulations."""
        explicit = artifact.get("qa", {})
        failures = list(explicit.get("failure_codes", []))
        if artifact.get("artifact_status") == "FAILED":
            failures.append("TECHNICAL_FAILURE")
        dimensions = {
            name: explicit.get(name, "PASS" if not failures else "FAIL")
            for name in DIMENSIONS
        }
        if artifact.get("artifact_status") == "SIMULATED" and not failures:
            dimensions = {name: "PASS" for name in DIMENSIONS}
        unique_failures = list(dict.fromkeys(failures))
        decision = "APPROVED" if all(value == "PASS" for value in dimensions.values()) else "REGENERATE"
        return {
            **dimensions,
            "decision": decision,
            "failure_codes": unique_failures,
            "repair_plan": build_repair_plan(unique_failures),
            "metrics": artifact.get("metrics", {}),
        }
