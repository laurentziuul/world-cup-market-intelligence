from __future__ import annotations

from pathlib import Path

import pandas as pd

WATCHLIST_COLUMNS = [
    "watchlist_id",
    "source",
    "event_slug",
    "market_slug",
    "market_type",
    "question",
    "outcome_focus",
    "priority",
    "why_track",
    "signal_bucket",
    "notes",
]

SEED_ROWS = [
    {
        "watchlist_id": "wc26-outright-001",
        "source": "polymarket",
        "event_slug": "world-cup-winner",
        "market_slug": "world-cup-winner",
        "market_type": "outright",
        "question": "Who will win the 2026 FIFA World Cup?",
        "outcome_focus": "favorites + dark horses",
        "priority": "high",
        "why_track": "Benchmark market for global narrative and crowd positioning.",
        "signal_bucket": "structural",
        "notes": "Replace slug after fetching live Gamma event data if needed.",
    },
    {
        "watchlist_id": "wc26-group-001",
        "source": "polymarket",
        "event_slug": "",
        "market_slug": "",
        "market_type": "group_advancement",
        "question": "Group winner / team advancement markets",
        "outcome_focus": "second-tier teams",
        "priority": "medium",
        "why_track": "Potentially less efficient than outright winner markets.",
        "signal_bucket": "tactical",
        "notes": "Populate after final market discovery.",
    },
    {
        "watchlist_id": "wc26-props-001",
        "source": "polymarket",
        "event_slug": "",
        "market_slug": "",
        "market_type": "player_props",
        "question": "Golden Boot / Golden Ball / player-specific props",
        "outcome_focus": "thin liquidity markets",
        "priority": "low",
        "why_track": "Useful for studying liquidity fragility, but higher noise.",
        "signal_bucket": "speculative",
        "notes": "Do not publish as pick without strong data.",
    },
]


def main() -> None:
    path = Path("data/watchlist.csv")
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        print(f"Watchlist already exists: {path}")
        return
    df = pd.DataFrame(SEED_ROWS, columns=WATCHLIST_COLUMNS)
    df.to_csv(path, index=False)
    print(f"Created {path}")


if __name__ == "__main__":
    main()
