from wcmi.scoring import classify_signal, score_market


def test_classify_signal_structural():
    signal_type, action = classify_signal(7)
    assert signal_type == "structural"
    assert action == "write"


def test_score_market_formula():
    score = score_market(
        market_slug="example",
        question="Example market?",
        price_move_score=3,
        liquidity_score=2,
        catalyst_score=2,
        narrative_crowding_penalty=1,
        failure_risk_penalty=1,
    )
    assert score.total_score == 5
    assert score.signal_type == "tactical"
