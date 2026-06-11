from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import requests

from wcmi.config import settings
from wcmi.models import MarketSnapshot


def _safe_float(value: Any) -> float | None:
    if value in (None, "", "NaN"):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def fetch_events(query: str | None = None, limit: int = 100) -> list[dict[str, Any]]:
    """Fetch active Polymarket events from Gamma API.

    The Gamma API is public and does not require authentication. This function is intentionally
    conservative and read-only.
    """
    params: dict[str, Any] = {
        "active": "true",
        "closed": "false",
        "limit": limit,
    }
    if query:
        params["q"] = query

    response = requests.get(f"{settings.gamma_base_url}/events", params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "events" in data:
        return data["events"]
    return []


def flatten_event_markets(events: list[dict[str, Any]]) -> list[MarketSnapshot]:
    snapshots: list[MarketSnapshot] = []
    now = datetime.now(timezone.utc)

    for event in events:
        event_slug = event.get("slug") or event.get("eventSlug")
        markets = event.get("markets") or []
        if not isinstance(markets, list):
            continue

        for market in markets:
            question = market.get("question") or market.get("title") or market.get("slug") or "Unknown market"
            outcomes = market.get("outcomes") or []
            outcome_prices = market.get("outcomePrices") or market.get("outcome_prices") or []

            # Gamma sometimes returns outcomePrices as strings or JSON-like lists.
            if isinstance(outcomes, str):
                outcomes = [outcomes]
            if isinstance(outcome_prices, str):
                # Do not eval. Keep fallback safe.
                outcome_prices = []

            if outcomes and isinstance(outcomes, list):
                for idx, outcome in enumerate(outcomes):
                    price = None
                    if isinstance(outcome_prices, list) and idx < len(outcome_prices):
                        price = _safe_float(outcome_prices[idx])
                    snapshots.append(
                        MarketSnapshot(
                            snapshot_ts=now,
                            event_slug=event_slug,
                            market_slug=market.get("slug"),
                            market_id=str(market.get("id") or market.get("conditionId") or ""),
                            question=question,
                            outcome=str(outcome),
                            current_price=price,
                            volume=_safe_float(market.get("volume") or market.get("volumeNum")),
                            liquidity=_safe_float(market.get("liquidity") or market.get("liquidityNum")),
                            active=market.get("active"),
                            closed=market.get("closed"),
                            raw={"event": event, "market": market},
                        )
                    )
            else:
                snapshots.append(
                    MarketSnapshot(
                        snapshot_ts=now,
                        event_slug=event_slug,
                        market_slug=market.get("slug"),
                        market_id=str(market.get("id") or market.get("conditionId") or ""),
                        question=question,
                        outcome=None,
                        current_price=_safe_float(market.get("lastTradePrice") or market.get("bestBid")),
                        volume=_safe_float(market.get("volume") or market.get("volumeNum")),
                        liquidity=_safe_float(market.get("liquidity") or market.get("liquidityNum")),
                        active=market.get("active"),
                        closed=market.get("closed"),
                        raw={"event": event, "market": market},
                    )
                )

    return snapshots


def fetch_world_cup_snapshots(query: str = "world cup", limit: int = 100) -> list[MarketSnapshot]:
    events = fetch_events(query=query, limit=limit)
    return flatten_event_markets(events)
