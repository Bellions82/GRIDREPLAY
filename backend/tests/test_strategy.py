from backend.director.strategy import GenerationStrategy, ProviderCapability

def test_strategy_uses_image_to_video_when_supported():
    cap = ProviderCapability(
        provider="test", model="model-a", model_version="1",
        image_to_video=True, reference_images=True, character_reference=True
    )
    result = GenerationStrategy().select({
        "references": ["ref_1"],
        "character_id": "char_1",
    }, cap)
    assert result["strategy"] == "IMAGE_TO_VIDEO"
    assert result["controls"]["use_reference_images"] is True
    assert result["controls"]["use_character_reference"] is True

def test_strategy_does_not_claim_unsupported_controls():
    cap = ProviderCapability(provider="test", model="model-a", model_version="1")
    result = GenerationStrategy().select({
        "references": ["ref_1"], "opening_frame": "frame_1", "camera": {"move": "dolly"}
    }, cap)
    assert result["strategy"] == "TEXT_TO_VIDEO"
    assert result["controls"]["use_reference_images"] is False
    assert result["controls"]["use_first_frame"] is False
    assert result["controls"]["use_camera_control"] is False
