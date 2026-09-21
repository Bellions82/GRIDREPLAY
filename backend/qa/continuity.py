from __future__ import annotations

from dataclasses import dataclass

DIMENSIONS = (
    "character",
    "wardrobe",
    "location",
    "visual_dna",
    "lighting",
    "screen_direction",
    "camera",
    "action",
    "props",
)

@dataclass(frozen=True)
class ContinuityPolicy:
    threshold: float = 0.90
    hard_fail_dimensions: tuple[str, ...] = ("character", "location", "visual_dna")

def _match(previous: dict, current: dict, key: str) -> float | None:
    a, b = previous.get(key), current.get(key)
    if a is None or b is None:
        return None
    return 1.0 if a == b else 0.0

def compare_shots(previous: dict, current: dict, *, policy: ContinuityPolicy | None = None) -> dict:
    policy = policy or ContinuityPolicy()
    scores = {key: _match(previous, current, key) for key in DIMENSIONS}

    # A missing value is unknown, not a failure. A contradictory locked value is a failure.
    hard_failures = [
        key for key in policy.hard_fail_dimensions
        if scores[key] == 0.0
    ]
    known = [v for v in scores.values() if v is not None]
    overall = sum(known) / len(known) if known else None

    failures = [key for key, value in scores.items() if value == 0.0]
    if hard_failures or (overall is not None and overall < policy.threshold):
        status = "REPAIR"
    elif overall is None:
        status = "UNKNOWN"
    else:
        status = "PASS"

    return {
        "status": status,
        "overall_score": overall,
        "threshold": policy.threshold,
        "scores": scores,
        "failures": failures,
        "hard_failures": hard_failures,
        "evidence": {
            "source": "declared_shot_state",
            "previous_shot_id": previous.get("shot_id"),
            "current_shot_id": current.get("shot_id"),
        },
    }
