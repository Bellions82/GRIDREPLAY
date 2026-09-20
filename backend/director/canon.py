from __future__ import annotations

from dataclasses import dataclass, field

@dataclass(frozen=True)
class CanonNode:
    id: str
    locked: bool = True
    constraints: dict = field(default_factory=dict)
    parent_id: str | None = None

class CanonViolation(ValueError):
    pass

def merge_canon(parent: dict, child: dict) -> dict:
    if not parent:
        return dict(child)
    merged = dict(parent)
    for key, value in child.items():
        if key in parent and parent[key] != value and parent.get("_locked", False):
            raise CanonViolation(f"locked canon conflict: {key}")
        merged[key] = value
    return merged
