"""
Real Schema Validator - DCA-01 Fusion Layer
Validates every expert output against JSON Schema Registry before fusion
"""
import json
from pathlib import Path
from jsonschema import validate, ValidationError, Draft7Validator
from typing import Dict, List, Tuple

SCHEMA_DIR = Path(__file__).parent.parent.parent / "schemas"

class SchemaRegistry:
    def __init__(self):
        self.schemas = {}
        self.validators = {}
        for schema_file in SCHEMA_DIR.glob("*.json"):
            with open(schema_file) as f:
                schema = json.load(f)
                self.schemas[schema_file.name] = schema
                self.validators[schema_file.name] = Draft7Validator(schema)
        print(f"[SchemaRegistry] Loaded {len(self.schemas)} schemas: {list(self.schemas.keys())}")

    def validate(self, instance: Dict, schema_name: str) -> Tuple[bool, str]:
        if schema_name not in self.schemas:
            return False, f"Schema {schema_name} not found in registry"
        try:
            validate(instance=instance, schema=self.schemas[schema_name])
            return True, "OK"
        except ValidationError as e:
            return False, f"Schema {schema_name} violation: {e.message} at path {'/'.join(map(str, e.path))}"

    def validate_expert_output(self, expert_output: Dict) -> Tuple[bool, str]:
        ok, msg = self.validate(expert_output, "expert_output_v1.json")
        if not ok:
            return ok, msg
        node_id = expert_output.get("node_id","")
        y_i = expert_output.get("y_i",{})
        if "physik" in node_id or "physics" in node_id:
            return self.validate(y_i, "physik_output_v1.json")
        if "code" in node_id:
            return self.validate(y_i, "code_output_v1.json")
        return True, "OK"

registry = SchemaRegistry()

def validate_units(physics_y: Dict, code_y: Dict) -> Tuple[bool, str]:
    if "h_coefficient" in physics_y:
        code_str = json.dumps(code_y)
        if "int(" in code_str and "h_coefficient" in code_str:
            return False, "UNIT_MISMATCH: physics requires float64 for h_coefficient, code uses int"
    return True, "OK"

def check_all(expert_outputs: List[Dict]) -> Tuple[bool, List[Dict]]:
    constraints = []
    for out in expert_outputs:
        ok, msg = registry.validate_expert_output(out)
        if not ok:
            constraints.append({
                "type": "FORMAT_VIOLATION",
                "detail": msg,
                "failing_module": out.get("module_id"),
                "expected": "expert_output_v1.json",
                "actual": out
            })
    return len(constraints)==0, constraints