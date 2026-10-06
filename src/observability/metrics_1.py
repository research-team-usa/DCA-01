# Prometheus metrics placeholder
from prometheus_client import Counter, Histogram, Gauge

router_disagreement = Counter("dca_router_disagreement_total", "TMR disagreements")
fusion_iterations = Histogram("dca_fusion_iterations", "Fusion iterations per DAG")
expert_latency = Histogram("dca_expert_latency_ms", "Expert latency", ["module"])
expert_ece = Gauge("dca_expert_ece_score", "ECE score", ["module"])