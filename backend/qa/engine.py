from __future__ import annotations

from backend.qa.repair import build_repair_plan

DIMENSIONS = ("technical", "visual", "character", "environment", "temporal", "timeline")

class QAEngine:
    """Structured deterministic gate. Provider-specific computer vision metrics plug in later."""

    def evaluate(self, artifact: dict) -> dict:
        explicit = artifact.get("qa", {})
        failures = list(explicit.get("failure_codes", []))

        if artifact.get("artifact_status") == "FAILED":
            failures.append("TECHNICAL_FAILURE")

        dimensions = {
            name: explicit.get(name, "PASS" if not failures else "FAIL")
            for name in DIMENSIONS
        }
        # A development simulation is intentionally passable so orchestration can be tested.
        if artifact.get("artifact_status") == "SIMULATED" and not failures:
            dimensions = {name: "PASS" for name in DIMENSIONS}

        decision = "APPROVED" if all(value == "PASS" for value in dimensions.values()) else "REGENERATE"
        return {
            **dimensions,
            "decision": decision,
            "failure_codes": failures,
            "repair_plan": build_repair_plan(failures),
            "metrics": artifact.get("metrics", {}),
        }
