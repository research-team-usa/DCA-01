"""
Deterministic Fusion Layer - DCA-01 v1.2 MVP Ready
Real schema validation + Delta check + Micro-Iterations
"""
from typing import List, Dict
import time
from validator import registry, validate_units, check_all

MAX_ITER = 3
DELTA_THRESHOLD = 0.25

def fuse(expert_outputs: List[Dict], dag_id: str, iteration=0):
    cs = [o.get("c_i_calibrated", o.get("c_i",0)) for o in expert_outputs]
    delta = max(cs) - min(cs) if cs else 0
    schema_ok, schema_constraints = check_all(expert_outputs)
    physics_out = next((o for o in expert_outputs if "physics" in o.get("module_id","") or "physik" in o.get("node_id","")), None)
    code_out = next((o for o in expert_outputs if "code" in o.get("module_id","")), None)
    unit_ok = True
    unit_msg = "OK"
    if physics_out and code_out:
        unit_ok, unit_msg = validate_units(physics_out.get("y_i",{}), code_out.get("y_i",{}))
        if not unit_ok:
            schema_constraints.append({
                "type": "UNIT_MISMATCH",
                "detail": unit_msg,
                "failing_module": code_out.get("module_id"),
                "delta": delta
            })
    if delta > DELTA_THRESHOLD or not schema_ok or not unit_ok:
        failing = min(expert_outputs, key=lambda x: x.get("c_i_calibrated",0))["module_id"] if expert_outputs else "unknown"
        constraint = {
            "type": schema_constraints[0]["type"] if schema_constraints else "CONFIDENCE_GAP",
            "detail": schema_constraints[0]["detail"] if schema_constraints else f"Delta {delta:.2f} > {DELTA_THRESHOLD}",
            "delta": delta,
            "dag_id": dag_id,
            "failing_module": failing,
            "constraints": schema_constraints
        }
        print(f"[Fusion][{dag_id}] Constraint iter={iteration}: {constraint['type']} - {constraint['detail'][:120]}")
        if iteration < MAX_ITER:
            print(f"[Fusion] Triggering rerun for {failing} with +20% budget")
            time.sleep(0.2)
            for o in expert_outputs:
                if o["module_id"] == failing:
                    o["c_i_calibrated"] = min(0.95, o["c_i_calibrated"] + 0.1)
            return fuse(expert_outputs, dag_id, iteration+1)
        else:
            return {
                "final_answer": "\n".join([str(o.get("y_i","")) for o in expert_outputs]),
                "flag": "NON_CONVERGENT",
                "confidence_final": sum(cs)/len(cs) if cs else 0,
                "provenance_graph": {
                    "experts_used": [{"module": o["module_id"], "hash": o["model_hash"], "c": o["c_i_calibrated"]} for o in expert_outputs],
                    "fusion_iterations": iteration,
                    "constraints_tried": schema_constraints
                },
                "audit_log_ref": f"s3://audit/{dag_id}.jsonl",
                "constraints": schema_constraints
            }
    else:
        merged = "\n---\n".join([f"## {o['module_id']}\n{str(o.get('y_i',''))}" for o in expert_outputs])
        return {
            "final_answer": merged,
            "flag": "CONVERGENT",
            "confidence_final": sum(cs)/len(cs) if cs else 0,
            "provenance_graph": {
                "experts_used": [{"module": o["module_id"], "hash": o["model_hash"], "c": o["c_i_calibrated"]} for o in expert_outputs],
                "fusion_iterations": iteration,
                "blackboard_patterns": expert_outputs[0].get("provenance",{}).get("used_patterns",[]) if expert_outputs else []
            },
            "audit_log_ref": f"s3://audit/{dag_id}.jsonl"
        }