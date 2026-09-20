from __future__ import annotations

class MotionPlanner:
    def plan(self, shot: dict) -> dict:
        return {
            "schema_version": "4.2",
            "motion": {
                "type": shot.get("motion_type", "cinematic"),
                "tempo": shot.get("motion_tempo", "moderate"),
                "beats": shot.get("action_beats", []),
                "acceleration": shot.get("acceleration", "medium"),
                "recovery": shot.get("recovery", "natural"),
                "intensity": float(shot.get("intensity", 0.5)),
            },
        }
