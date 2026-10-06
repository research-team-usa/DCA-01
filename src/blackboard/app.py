from fastapi import FastAPI
from pydantic import BaseModel
from blackboard import Blackboard
app = FastAPI(title="DCA-01 Blackboard")
board = Blackboard()
class PatternIn(BaseModel):
    pattern_id: str
    dag_id: str
    source_module: str
    pattern_type: str
    abstraction: dict
    source_model_hash: str = "sha256:test"
    ttl_ms: int = 5000
@app.post("/publish")
def publish(p: PatternIn):
    return {"ok": board.publish(p.dict()), "pattern_id": p.pattern_id}
@app.get("/patterns/{dag_id}")
def get_patterns(dag_id: str):
    return [x for x in board.subscribe() if x.get("dag_id")==dag_id]
@app.get("/health")
def health():
    return {"status":"ok","count": len(board.patterns)}
