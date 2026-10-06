def infer(node, *args):
    return {
        "node_id": node["node_id"],
        "module_id": "language_expert_v1.0",
        "model_hash": "sha256:lang_v1.0",
        "y_i": {"text": "Final documentation and explanation of heat exchanger simulation."},
        "c_i": 0.96,
        "c_i_calibrated": 0.94,
        "t_i_ms": 120,
        "provenance": {"used_patterns":[]}
    }