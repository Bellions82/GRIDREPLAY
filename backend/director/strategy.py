from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class ProviderCapability:
    provider: str
    model: str
    model_version: str
    text_to_video: bool = False
    image_to_video: bool = False
    first_frame: bool = False
    last_frame: bool = False
    reference_images: bool = False
    character_reference: bool = False
    camera_control: bool = False
    seed: bool = False
    max_duration_seconds: float = 0.0

@dataclass(frozen=True)
class ShotDifficulty:
    identity_risk: float
    motion_risk: float
    temporal_risk: float
    composition_risk: float
    sync_risk: float

    @property
    def overall(self) -> float:
        values = (self.identity_risk, self.motion_risk, self.temporal_risk, self.composition_risk, self.sync_risk)
        return sum(values) / len(values)

class GenerationStrategy:
    """Chooses generation controls from shot risk and actual provider capabilities."""
    def select(self, shot: dict, capability: ProviderCapability) -> dict:
        difficulty = ShotDifficulty(
            identity_risk=float(shot.get("identity_risk", 0.0)),
            motion_risk=float(shot.get("motion_risk", 0.0)),
            temporal_risk=float(shot.get("temporal_risk", 0.0)),
            composition_risk=float(shot.get("composition_risk", 0.0)),
            sync_risk=float(shot.get("sync_risk", 0.0)),
        )
        references = bool(shot.get("references"))
        use_i2v = references and capability.image_to_video
        return {
            "strategy": "IMAGE_TO_VIDEO" if use_i2v else "TEXT_TO_VIDEO",
            "difficulty": difficulty.overall,
            "risk": {
                "identity": difficulty.identity_risk,
                "motion": difficulty.motion_risk,
                "temporal": difficulty.temporal_risk,
                "composition": difficulty.composition_risk,
                "sync": difficulty.sync_risk,
            },
            "controls": {
                "use_reference_images": references and capability.reference_images,
                "use_character_reference": bool(shot.get("character_id")) and capability.character_reference,
                "use_first_frame": capability.first_frame and bool(shot.get("opening_frame")),
                "use_last_frame": capability.last_frame and bool(shot.get("closing_frame")),
                "use_camera_control": capability.camera_control and bool(shot.get("camera")),
                "deterministic_seed": capability.seed and shot.get("seed") is not None,
            },
        }
