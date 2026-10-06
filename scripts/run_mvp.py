"""
DCA-01 MVP Runner - End-to-End without Docker
"""
import sys
sys.path.append("src/router")
sys.path.append("src/decomposer")
sys.path.append("src/blackboard")
sys.path.append("src/experts/physics")
sys.path.append("src/experts/code")
sys.path.append("src/experts/language")
sys.path.append("src/fusion")
from tmr_router import Router, tmr_vote
from dag_builder import build_dag
from blackboard import Blackboard
from physics_expert import infer as physics_infer
from code_expert import infer as code_infer
from language_expert import infer as lang_infer
from fusion import fuse
import json
def run(request: str):
    print(f"\n=== DCA-01 MVP Run ===\nRequest: {request}\n")
    print("[1] TMR Router Cluster")
    ra = Router("router_a","sha256:a").infer(request)
    rb = Router("router_b","sha256:b").infer(request)
    rc = Router("router_c","sha256:c").infer(request)
    vote = tmr_vote(ra, rb, rc)
    print(f"  -> {vote['flag']}")
    print("\n[2] Task Decomposer")
    dag_nodes = build_dag(vote["validated"], request)
    dag_id = dag_nodes[0]["dag_id"]
    print(f"  -> DAG {dag_id} nodes: {[n["node_id"] for n in dag_nodes]}")
    print("\n[3] Shared Context Board")
    board = Blackboard()
    pattern = {"pattern_id":"CLOSED_LOOP_01","version":"1.0","dag_id":dag_id,"source_module":"physics_expert","source_model_hash":"sha256:physics_v2.1","ttl_ms":5000,"pattern_type":"topological","abstraction":{"name":"closed loop","properties":{"conservation":True}},"vector_embedding":[0.1,0.9],"access_control":{"write":["physics_expert"],"read":["code_expert"]},"audit":True}
    board.publish(pattern)
    print(f"  -> Published {pattern['pattern_id']}")
    print("\n[4] Experts (parallel)")
    phys_out = physics_infer(dag_nodes[0], board.subscribe())
    code_out = code_infer(dag_nodes[1], phys_out, board.subscribe())
    lang_out = lang_infer({"node_id":"T_lang_01"})
    print(f"  -> Physics c={phys_out['c_i_calibrated']} Code c={code_out['c_i_calibrated']}")
    print("\n[5] Fusion Layer")
    result = fuse([phys_out, code_out, lang_out], dag_id)
    print(f"  -> Flag: {result['flag']} conf={result['confidence_final']:.2f} iters={result['provenance_graph']['fusion_iterations']}")
    print("\n=== Final Answer ===\n", result["final_answer"][:800])
    return result
if __name__ == "__main__":
    run("Write Python simulation for heat exchanger water/water with Q_dot 15kW")
