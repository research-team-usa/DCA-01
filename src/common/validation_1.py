import json, jsonschema
from pathlib import Path

def validate_against_schema(instance: dict, schema_name: str):
    schema_path = Path(__file__).parent.parent.parent / "schemas" / schema_name
    with open(schema_path) as f:
        schema = json.load(f)
    jsonschema.validate(instance, schema)
    return True