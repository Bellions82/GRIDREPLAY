from backend.qa.continuity import compare_shots

def test_locked_identity_mismatch_requires_repair():
    result = compare_shots(
        {"shot_id":"a","character_id":"char_1","location_id":"loc_1","visual_dna_id":"dna_1"},
        {"shot_id":"b","character_id":"char_2","location_id":"loc_1","visual_dna_id":"dna_1"},
    )
    assert result["status"] == "REPAIR"
    assert "character" in result["hard_failures"]

def test_unknown_is_not_failure():
    result = compare_shots(
        {"shot_id":"a","character_id":"char_1"},
        {"shot_id":"b","character_id":"char_1"},
    )
    assert result["status"] in ("PASS", "UNKNOWN")
    assert result["scores"]["location"] is None

def test_soft_dimension_can_trigger_repair():
    result = compare_shots(
        {"shot_id":"a","character_id":"char_1","location_id":"loc_1","visual_dna_id":"dna_1","camera":"wide","action":"walk"},
        {"shot_id":"b","character_id":"char_1","location_id":"loc_1","visual_dna_id":"dna_1","camera":"close","action":"run"},
    )
    assert result["status"] == "REPAIR"
    assert "camera" in result["failures"]
