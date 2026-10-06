from fastapi import FastAPI
from pydantic import BaseModel
from tmr_router import Router, tmr_vote
app = FastAPI(title="DCA-01 TMR Router")
class RequestIn(BaseModel):
    request: str
router_a = Router("router_a_v1.2", "sha256:a1b2c3")
router_b = Router("router_b_v1.2", "sha256:b2c3d4")
router_c = Router("router_c_v1.2", "sha256:c3d4e5")
@app.post("/route")
def route(req: RequestIn):
    ra = router_a.infer(req.request)
    rb = router_b.infer(req.request)
    rc = router_c.infer(req.request)
    return tmr_vote(ra, rb, rc)
@app.get("/health")
def health():
    return {"status":"ok"}
