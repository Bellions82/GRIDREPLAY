from backend.qa.engine import QAEngine
from backend.qa.repair import build_repair_plan

def test_simulated_artifact_can_pass_for_orchestration():
    result = QAEngine().evaluate({"artifact_status": "SIMULATED"})
    assert result["decision"] == "APPROVED"
    assert result["failure_codes"] == []

def test_explicit_failure_creates_repair_plan():
    result = QAEngine().evaluate({
        "artifact_status": "SIMULATED",
        "qa": {"failure_codes": ["IDENTITY_DRIFT", "MOTION_FAILURE"]},
    })
    assert result["decision"] == "REGENERATE"
    assert result["repair_plan"]["required"] is True
    actions = [item["action"] for item in result["repair_plan"]["actions"]]
    assert "REGENERATE_WITH_LOCKED_REFERENCE" in actions
    assert "ALTER_MOTION_SPEC_AND_REGENERATE" in actions

def test_unknown_failure_routes_to_human_review():
    plan = build_repair_plan(["UNKNOWN_FAILURE"])
    assert plan["actions"][0]["action"] == "HUMAN_REVIEW"
