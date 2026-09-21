from __future__ import annotations

from dataclasses import dataclass, field

@dataclass
class ApprovedState:
    shot_id: str
    state: dict
    generation_version: int

@dataclass
class ContinuityGraph:
    approved: dict[str, ApprovedState] = field(default_factory=dict)

    def approve(self, shot_id: str, state: dict, generation_version: int) -> None:
        self.approved[shot_id] = ApprovedState(shot_id, dict(state), generation_version)

    def get_reference(self, shot_id: str) -> ApprovedState | None:
        return self.approved.get(shot_id)

    def latest_approved_before(self, ordinal: int, shots: list[dict]) -> ApprovedState | None:
        candidates = [
            self.approved[s["shot_id"]]
            for s in shots
            if s.get("ordinal", -1) < ordinal and s.get("shot_id") in self.approved
        ]
        return max(candidates, key=lambda x: next(
            (s.get("ordinal", -1) for s in shots if s.get("shot_id") == x.shot_id), -1
        ), default=None)
