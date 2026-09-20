from __future__ import annotations

def compare_shots(previous: dict, current: dict) -> dict:
    checks = {
        "character": previous.get("character_id") == current.get("character_id"),
        "location": previous.get("location_id") == current.get("location_id"),
        "visual_dna": previous.get("visual_dna_id") == current.get("visual_dna_id"),
    }
    passed = all(checks.values())
    return {"status": "PASS" if passed else "REPAIR", "checks": checks}
