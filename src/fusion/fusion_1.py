"""
Deterministic Fusion Layer - DCA-01
Delta check + micro-iterations
"""
from typing import List, Dict

MAX_ITER = 3
DELTA_THRESHOLD = 0.25

def validate_units(outputs: List[Dict]) -> bool:
    # placeholder - check units
    return True

def validate_schema(outputs: List[Dict]) -> bool:
    return True

def fuse(expert_outputs: List[Dict], dag_id: str, iteration=0):
    cs = [o["c_i_calibrated"] for o in expert_outputs]
    delta = max(cs) - min(cs) if cs else 0

    type_ok = validate_schema(expert_outputs)
    unit_ok = validate_units(expert_outputs)

    if delta > DELTA_THRESHOLD or not type_ok or not unit_ok:
        constraint = {
            "type": "CONFIDENCE_GAP" if delta>DELTA_THRESHOLD else "TYPE_MISMATCH",
            "detail": f"Delta {delta:.2f} > threshold or schema fail. float64 required, int found. Pattern CLOSED_LOOP requires while with convergence.",
            "delta": delta,
            "dag_id": dag_id,
            "failing_module": min(expert_outputs, key=lambda x: x["c_i_calibrated"])["module_id"] if expert_outputs else "unknown"
        }
        if iteration < MAX_ITER:
            # trigger rerun only failing module (placeholder)
            print(f"[Fusion] Constraint {constraint} -> rerun {constraint['failing_module']} iter {iteration+1}")
            # In real system: call failing module again with constraint as extra input
            # For demo: just return with increased confidence simulation
            return fuse(expert_outputs, dag_id, iteration+1)
        else:
            return {
                "final_answer": "Best effort merge after max iter",
                "flag": "NON_CONVERGENT",
                "confidence_final": sum(cs)/len(cs) if cs else 0,
                "provenance_graph": {"fusion_iterations": iteration, "constraints": [constraint]},
                "audit_log_ref": f"s3://audit/{dag_id}.jsonl"
            }
    else:
        merged_text = "\n".join([str(o["y_i"]) for o in expert_outputs])
        return {
            "final_answer": merged_text,
            "flag": "CONVERGENT",
            "confidence_final": sum(cs)/len(cs) if cs else 0,
            "provenance_graph": {
                "experts_used": [{"module": o["module_id"], "hash": o["model_hash"], "c": o["c_i_calibrated"]} for o in expert_outputs],
                "fusion_iterations": iteration
            },
            "audit_log_ref": f"s3://audit/{dag_id}.jsonl"
        }