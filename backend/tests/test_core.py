from backend.core.fingerprint import render_fingerprint
from backend.core.state import RenderState,can_transition

def test_fingerprint_is_stable():
    a={'b':2,'a':1};assert render_fingerprint(a)==render_fingerprint({'a':1,'b':2})
def test_state_machine():
    assert can_transition(RenderState.CREATED,RenderState.QUEUED)
    assert not can_transition(RenderState.COMPLETED,RenderState.QUEUED)
