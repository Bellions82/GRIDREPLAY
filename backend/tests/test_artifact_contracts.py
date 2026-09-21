import json
from pathlib import Path

def test_artifact_schema_has_required_provenance_fields():
    schema = json.loads(Path("shared/schemas/artifact.schema.json").read_text())
    assert "artifact_status" in schema["required"]
    assert "media_type" in schema["required"]
    assert "provider" in schema["properties"]
    assert "model_version" in schema["properties"]
