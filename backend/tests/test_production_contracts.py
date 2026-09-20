from backend.director.canon import CanonViolation, merge_canon
from backend.director.motion import MotionPlanner
from backend.director.prompt_compiler import PromptCompiler

def test_locked_canon_conflict():
    try:
        merge_canon({"_locked": True, "costume": "black"}, {"costume": "white"})
        assert False
    except CanonViolation:
        assert True

def test_motion_plan():
    result = MotionPlanner().plan({"motion_type":"run","action_beats":["start","sprint"]})
    assert result["motion"]["beats"] == ["start","sprint"]

def test_prompt_compiler_contains_sections():
    result = PromptCompiler().compile(
        canon={"character":"locked"},
        scene={"location":"rooftop"},
        shot={"action":"turn"},
        motion={"type":"walk"},
    )
    assert "CANON:" in result["prompt"]
    assert "MOTION:" in result["prompt"]
