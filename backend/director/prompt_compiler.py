from __future__ import annotations

from dataclasses import dataclass

@dataclass
class PromptCompiler:
    def compile(
        self,
        *,
        canon: dict,
        scene: dict,
        shot: dict,
        motion: dict,
        composition: dict | None = None,
        continuity_reference: dict | None = None,
        repair: dict | None = None,
    ) -> dict:
        sections = [
            ("CANON", canon),
            ("SCENE", scene),
            ("SHOT", shot),
            ("MOTION", motion),
            ("COMPOSITION", composition or {}),
            ("APPROVED_CONTINUITY_REFERENCE", continuity_reference or {}),
            ("REPAIR_DIRECTIVES", repair or {}),
        ]
        prompt = "\n\n".join(
            f"{name}:\n{value}" for name, value in sections if value
        )
        return {
            "prompt": prompt,
            "negative_prompt": shot.get("negative_prompt", ""),
            "provider_payload": {
                "prompt": prompt,
                "negative_prompt": shot.get("negative_prompt", ""),
            },
        }
