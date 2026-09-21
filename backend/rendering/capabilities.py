from __future__ import annotations

from backend.director.strategy import ProviderCapability

class CapabilityRegistry:
    def __init__(self, capabilities: list[ProviderCapability] | None = None):
        self._items = {(x.provider, x.model, x.model_version): x for x in (capabilities or [])}

    def register(self, capability: ProviderCapability) -> None:
        self._items[(capability.provider, capability.model, capability.model_version)] = capability

    def get(self, provider: str, model: str, model_version: str = "") -> ProviderCapability | None:
        return self._items.get((provider, model, model_version)) or self._items.get((provider, model, ""))

    def choose(self, model: str, *, require_image_to_video: bool = False) -> ProviderCapability | None:
        matches = [x for x in self._items.values() if x.model == model]
        if require_image_to_video:
            matches = [x for x in matches if x.image_to_video]
        return matches[0] if matches else None
