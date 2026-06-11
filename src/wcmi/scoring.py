from __future__ import annotations

from wcmi.models import ActionType, SignalScore, SignalType


def classify_signal(total_score: int) -> tuple[SignalType, ActionType]:
    if total_score >= 7:
        return "structural", "write"
    if total_score >= 4:
        return "tactical", "research"
    if total_score >= 2:
        return "speculative", "watch"
    return "noise", "ignore"


def score_market(
    *,
    market_slug: str | None,
    question: str,
    price_move_score: int = 0,
    liquidity_score: int = 0,
    catalyst_score: int = 0,
    narrative_crowding_penalty: int = 0,
    failure_risk_penalty: int = 0,
    rationale: str = "Manual v0 score.",
) -> SignalScore:
    """Transparent v0 heuristic scoring.

    Formula:
        total = price_move + liquidity + catalyst - narrative_crowding - failure_risk

    The goal is not to predict winners. The goal is to prioritize which market changes
    deserve research and publication.
    """
    total = (
        price_move_score
        + liquidity_score
        + catalyst_score
        - narrative_crowding_penalty
        - failure_risk_penalty
    )
    signal_type, action = classify_signal(total)
    return SignalScore(
        market_slug=market_slug,
        question=question,
        price_move_score=price_move_score,
        liquidity_score=liquidity_score,
        catalyst_score=catalyst_score,
        narrative_crowding_penalty=narrative_crowding_penalty,
        failure_risk_penalty=failure_risk_penalty,
        total_score=total,
        signal_type=signal_type,
        action=action,
        rationale=rationale,
    )
