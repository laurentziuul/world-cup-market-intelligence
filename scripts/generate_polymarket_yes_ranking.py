from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from wcmi.providers.polymarket import PolymarketProvider


ROOT = Path(__file__).resolve().parents[1]

OUTPUT_DIR = ROOT / "data" / "processed"
RANKING_PATH = OUTPUT_DIR / "polymarket_worldcup_yes_ranking.csv"
SUMMARY_PATH = OUTPUT_DIR / "polymarket_worldcup_yes_ranking_summary.txt"

WINNER_MARKET_PATTERN = re.compile(
    r"^Will (.+) win the 2026 FIFA World Cup\?$",
    re.IGNORECASE,
)


OUTPUT_COLUMNS = [
    "rank",
    "team",
    "yes_probability",
    "yes_probability_display",
    "market_title",
    "volume",
    "liquidity",
    "source_url",
    "provider",
]


def extract_team_name(market_title: str) -> str:
    match = WINNER_MARKET_PATTERN.match(str(market_title).strip())

    if not match:
        return ""

    return match.group(1).strip()


def format_probability(value: float) -> str:
    return f"{value * 100:.2f}%"


def build_yes_ranking(dataframe: pd.DataFrame) -> pd.DataFrame:
    if dataframe.empty:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)

    working = dataframe.copy()

    working["team"] = working["market_title"].apply(extract_team_name)

    ranking = working[
        (working["team"] != "")
        & (working["outcome"].str.lower() == "yes")
    ].copy()

    if ranking.empty:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)

    ranking["yes_probability"] = pd.to_numeric(
        ranking["price"],
        errors="coerce",
    ).fillna(0.0)

    ranking["volume"] = pd.to_numeric(
        ranking["volume"],
        errors="coerce",
    ).fillna(0.0)

    ranking["liquidity"] = pd.to_numeric(
        ranking["liquidity"],
        errors="coerce",
    ).fillna(0.0)

    ranking = ranking.sort_values(
        by=["yes_probability", "volume", "liquidity"],
        ascending=[False, False, False],
    ).reset_index(drop=True)

    ranking["rank"] = ranking.index + 1
    ranking["yes_probability_display"] = ranking["yes_probability"].apply(
        format_probability
    )
    ranking["provider"] = "polymarket"

    return ranking[OUTPUT_COLUMNS]


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    print("Polymarket YES-only World Cup ranking")
    print("Fetching experimental Polymarket provider data...")
    print("")

    provider = PolymarketProvider()
    dataframe = provider.load()

    ranking = build_yes_ranking(dataframe)

    ranking.to_csv(RANKING_PATH, index=False)

    lines = []
    lines.append("Polymarket YES-only World Cup ranking summary")
    lines.append(f"Timestamp UTC: {timestamp}")
    lines.append(f"Provider rows loaded: {len(dataframe)}")
    lines.append(f"YES ranking rows: {len(ranking)}")
    lines.append("")
    lines.append("Top teams:")

    if ranking.empty:
        lines.append("No YES winner markets found.")
    else:
        for _, row in ranking.head(25).iterrows():
            lines.append(
                f"{int(row['rank'])}. "
                f"{row['team']} — "
                f"{row['yes_probability_display']} "
                f"| volume={row['volume']:.2f} "
                f"| liquidity={row['liquidity']:.2f}"
            )

    SUMMARY_PATH.write_text("\n".join(lines), encoding="utf-8")

    print("\n".join(lines))
    print("")
    print(f"Saved ranking: {RANKING_PATH}")
    print(f"Saved summary: {SUMMARY_PATH}")


if __name__ == "__main__":
    main()