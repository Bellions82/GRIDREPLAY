import pytest

from backend.qa.metrics import evaluate_thresholds
from backend.qa.visual_inspector import VisualInspector
from backend.qa.technical import TechnicalInspector

@pytest.mark.asyncio
async def test_inspection_contracts_preserve_unknowns():
    visual = await VisualInspector().inspect({"inspection": {}})
    technical = await TechnicalInspector().inspect({"technical": {}})
    assert visual["identity_similarity"] is None
    assert technical["playable"] is None

def test_thresholds_report_unknown_and_failures():
    result = evaluate_thresholds(
        {"identity_similarity": 0.91, "temporal_stability": 0.72},
        {"identity_similarity": 0.90, "temporal_stability": 0.80},
    )
    assert result["results"]["identity_similarity"]["status"] == "PASS"
    assert result["results"]["temporal_stability"]["status"] == "FAIL"
    assert "temporal_stability" in result["failures"]
