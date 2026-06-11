from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

SignalType = Literal["structural", "tactical", "speculative", "noise"]
ActionType = Literal["watch", "write", "ignore", "research"]


class MarketSnapshot(BaseModel):
    snapshot_ts: datetime
    source: str = "polymarket_gamma"
    event_slug: str | None = None
    market_slug: str | None = None
    market_id: str | None = None
    question: str
    outcome: str | None = None
    current_price: float | None = None
    volume: float | None = None
    liquidity: float | None = None
    spread: float | None = None
    active: bool | None = None
    closed: bool | None = None
    raw: dict[str, Any] = Field(default_factory=dict)


class SignalScore(BaseModel):
    market_slug: str | None
    question: str
    price_move_score: int
    liquidity_score: int
    catalyst_score: int
    narrative_crowding_penalty: int
    failure_risk_penalty: int
    total_score: int
    signal_type: SignalType
    action: ActionType
    rationale: str
