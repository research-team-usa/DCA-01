"""
Task Decomposer - Builds DAG from validated intent
"""
import hashlib, json
from typing import List

def build_dag(validated_intent: dict, request: str) -> List[dict]:
    dag_id = f"dag_{hashlib.sha256(request.encode()).hexdigest()[:12]}"
    nodes = [
        {
            "node_id": "T_physik_01",
            "dag_id": dag_id,
            "domain": "thermodynamics",
            "objective": "calculate heat transfer coefficient",
            "target_hardware": "hpc_h100",
            "compute_budget_ms": 800,
            "timeout_ms": 1200,
            "retries": 1,
            "priority": 1,
            "output_spec": {
                "format": "json",
                "schema_ref": "schemas/physik_output_v1.json",
                "required_fields": ["Q_dot","delta_T"],
                "determinism": {"temperature":0,"seed":42,"top_p":1.0,"top_k":1}
            },
            "dependencies": [],
            "blackboard_subscriptions": ["CLOSED_LOOP"]
        },
        {
            "node_id": "T_code_01",
            "dag_id": dag_id,
            "domain": "code_generation",
            "objective": "write Python simulation using physics output",
            "target_hardware": "a6000",
            "compute_budget_ms": 600,
            "timeout_ms": 1000,
            "retries": 1,
            "priority": 2,
            "output_spec": {
                "format": "json",
                "schema_ref": "schemas/code_output_v1.json",
                "required_fields": ["language","code"],
                "determinism": {"temperature":0,"seed":42}
            },
            "dependencies": ["T_physik_01"],
            "blackboard_subscriptions": ["CLOSED_LOOP"]
        }
    ]
    return nodes