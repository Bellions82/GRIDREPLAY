from backend.core.fingerprint import render_fingerprint
from backend.core.state import RenderState, can_transition


def test_render_fingerprint_is_deterministic():
    a = {"project_id": "p", "model": "m", "params": {"steps": 20}}
    b = {"params": {"steps": 20}, "model": "m", "project_id": "p"}
    assert render_fingerprint(a) == render_fingerprint(b)


def test_render_state_supports_recovery_cycle():
    assert can_transition(RenderState.REGENERATE, RenderState.QUEUED)
    assert can_transition(RenderState.QUEUED, RenderState.CLAIMED)
    assert can_transition(RenderState.CLAIMED, RenderState.PROCESSING)
