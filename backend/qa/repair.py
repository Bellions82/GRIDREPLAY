from __future__ import annotations

REPAIR_ACTIONS = {
    "IDENTITY_DRIFT": {"action": "REGENERATE_WITH_LOCKED_REFERENCE", "priority": "high"},
    "WARDROBE_DRIFT": {"action": "REGENERATE_WITH_CANON_WARDROBE", "priority": "high"},
    "FACE_DRIFT": {"action": "REGENERATE_WITH_IDENTITY_REFERENCE", "priority": "high"},
    "ANATOMY": {"action": "SHORTEN_OR_CROP_OR_REGENERATE", "priority": "high"},
    "HAND_FAILURE": {"action": "CROP_OR_REGENERATE", "priority": "high"},
    "PROP_FAILURE": {"action": "REGENERATE_WITH_PROP_LOCK", "priority": "medium"},
    "BACKGROUND_DRIFT": {"action": "REPLACE_BACKGROUND_OR_REGENERATE", "priority": "medium"},
    "LOCATION_DRIFT": {"action": "REGENERATE_WITH_LOCATION_LOCK", "priority": "high"},
    "MOTION_FAILURE": {"action": "ALTER_MOTION_SPEC_AND_REGENERATE", "priority": "high"},
    "TEMPORAL_FLICKER": {"action": "STABILIZE_OR_RERENDER", "priority": "high"},
    "PHYSICS_FAILURE": {"action": "SHORTEN_OR_REGENERATE", "priority": "medium"},
    "COMPOSITION_FAILURE": {"action": "REFRAME_OR_REGENERATE", "priority": "medium"},
    "LYRIC_MISMATCH": {"action": "REPLAN_SHOT", "priority": "high"},
    "BEAT_MISMATCH": {"action": "RETIME_OR_REPLAN_SHOT", "priority": "high"},
    "AUDIO_SYNC": {"action": "RETIME_AND_REASSEMBLE", "priority": "high"},
    "TECHNICAL_FAILURE": {"action": "RERENDER", "priority": "high"},
}

def build_repair_plan(failure_codes: list[str]) -> dict:
    actions = [REPAIR_ACTIONS.get(code, {"action": "HUMAN_REVIEW", "priority": "high"}) for code in failure_codes]
    return {"required": bool(failure_codes), "actions": actions, "failure_codes": failure_codes}
