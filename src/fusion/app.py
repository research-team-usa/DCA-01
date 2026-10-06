from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from fusion import fuse
app = FastAPI(title="DCA-01 Fusion")
class FusionRequest(BaseModel):
    dag_id: str
    expert_outputs: List[Dict]
@app.post("/fuse")
def fuse_endpoint(req: FusionRequest):
    return fuse(req.expert_outputs, req.dag_id)
@app.get("/health")
def health():
    return {"status":"ok"}
