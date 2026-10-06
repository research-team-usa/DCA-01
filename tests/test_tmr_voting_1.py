from src.router.tmr_router import tmr_vote

def test_tmr_majority():
    ra = {"dag_proposal":{"dag_hash":"abc"},"confidence_r":0.9}
    rb = {"dag_proposal":{"dag_hash":"abc"},"confidence_r":0.8}
    rc = {"dag_proposal":{"dag_hash":"xyz"},"confidence_r":0.7}
    result = tmr_vote(ra, rb, rc)
    assert result["flag"] == "CONVERGENT"

def test_tmr_disagreement():
    ra = {"dag_proposal":{"dag_hash":"a"},"confidence_r":0.9}
    rb = {"dag_proposal":{"dag_hash":"b"},"confidence_r":0.8}
    rc = {"dag_proposal":{"dag_hash":"c"},"confidence_r":0.7}
    result = tmr_vote(ra, rb, rc)
    assert result["flag"] == "TMR_DISAGREEMENT"