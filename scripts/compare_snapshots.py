from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

DEFAULT_SNAPSHOT_DIR = ROOT / "data" / "processed" / "snapshots"
DEFAULT_OUTPUT_PATH = ROOT / "data" / "processed" / "snapshot_comparison_latest.csv"


WINNER_MARKET_PREFIX = "Will "
WINNER_MARKET_SUFFIX = " win the 2026 FIFA World Cup?"


OUTPUT_COLUMNS = [
    "comparison_timestamp",
    "provider",
    "comparison_key",
    "team",
    "market_id",
    "market_title",
    "outcome",
    "status",
    "previous_probability",
    "current_probability",
    "probability_change",
    "probability_change_pp",
    "previous_volume",
    "current_volume",
    "volume_change",
    "previous_liquidity",
    "current_liquidity",
    "liquidity_change",
    "source_url",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare two processed prediction-market snapshots.",
    )
    parser.add_argument(
        "--provider",
        default="",
        help="Optional provider filter, for example: manual_csv or polymarket.",
    )
    parser.add_argument(
        "--snapshot-dir",
        default=str(DEFAULT_SNAPSHOT_DIR),
        help="Directory containing processed snapshot CSV files.",
    )
    parser.add_argument(
        "--previous",
        default="",
        help="Optional explicit previous snapshot CSV path.",
    )
    parser.add_argument(
        "--current",
        default="",
        help="Optional explicit current snapshot CSV path.",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_PATH),
        help="Output CSV path for the comparison result.",
    )
    return parser.parse_args()


def find_snapshot_pair(
    snapshot_dir: Path,
    provider: str,
    previous_path: str,
    current_path: str,
) -> tuple[Path, Path]:
    if previous_path and current_path:
        return Path(previous_path), Path(current_path)

    candidates = sorted(snapshot_dir.glob("*.csv"))

    if provider:
        provider_lower = provider.lower()
        candidates = [
            path
            for path in candidates
            if provider_lower in path.name.lower()
        ]

    if len(candidates) < 2:
        raise SystemExit(
            "Need at least two snapshot CSV files to compare. "
            "Pass --previous and --current explicitly, or generate more snapshots."
        )

    return candidates[-2], candidates[-1]


def pick_column(dataframe: pd.DataFrame, candidates: list[str]) -> str:
    lower_to_original = {
        column.lower(): column
        for column in dataframe.columns
    }

    for candidate in candidates:
        if candidate.lower() in lower_to_original:
            return lower_to_original[candidate.lower()]

    return ""


def extract_team_from_title(market_title: str) -> str:
    title = str(market_title).strip()

    if title.startswith(WINNER_MARKET_PREFIX) and title.endswith(WINNER_MARKET_SUFFIX):
        return title[
            len(WINNER_MARKET_PREFIX):-len(WINNER_MARKET_SUFFIX)
        ].strip()

    return ""


def normalize_snapshot(dataframe: pd.DataFrame, provider_filter: str) -> pd.DataFrame:
    working = dataframe.copy()

    provider_col = pick_column(working, ["provider"])
    market_id_col = pick_column(working, ["market_id", "conditionId", "condition_id", "id"])
    market_title_col = pick_column(working, ["market_title", "question", "title", "market"])
    team_col = pick_column(working, ["team", "asset", "selection"])
    outcome_col = pick_column(working, ["outcome", "side"])
    price_col = pick_column(working, ["price", "probability", "implied_probability", "yes_probability"])
    volume_col = pick_column(working, ["volume", "volumeNum", "volume_num"])
    liquidity_col = pick_column(working, ["liquidity", "liquidityNum", "liquidity_num"])
    source_url_col = pick_column(working, ["source_url", "url", "market_url"])

    normalized = pd.DataFrame()

    if provider_col:
        normalized["provider"] = working[provider_col].astype(str)
    else:
        normalized["provider"] = provider_filter or "unknown"

    if market_id_col:
        normalized["market_id"] = working[market_id_col].astype(str)
    else:
        normalized["market_id"] = ""

    if market_title_col:
        normalized["market_title"] = working[market_title_col].astype(str)
    else:
        normalized["market_title"] = ""

    if team_col:
        normalized["team"] = working[team_col].astype(str)
    else:
        normalized["team"] = normalized["market_title"].apply(extract_team_from_title)

    if outcome_col:
        normalized["outcome"] = working[outcome_col].astype(str)
    else:
        normalized["outcome"] = ""

    if price_col:
        normalized["probability"] = pd.to_numeric(
            working[price_col],
            errors="coerce",
        ).fillna(0.0)
    else:
        normalized["probability"] = 0.0

    if volume_col:
        normalized["volume"] = pd.to_numeric(
            working[volume_col],
            errors="coerce",
        ).fillna(0.0)
    else:
        normalized["volume"] = 0.0

    if liquidity_col:
        normalized["liquidity"] = pd.to_numeric(
            working[liquidity_col],
            errors="coerce",
        ).fillna(0.0)
    else:
        normalized["liquidity"] = 0.0

    if source_url_col:
        normalized["source_url"] = working[source_url_col].astype(str)
    else:
        normalized["source_url"] = ""

    if provider_filter:
        normalized = normalized[
            normalized["provider"].str.lower() == provider_filter.lower()
        ].copy()

    normalized["comparison_key"] = normalized.apply(build_comparison_key, axis=1)

    return normalized


def build_comparison_key(row: pd.Series) -> str:
    provider = str(row.get("provider", "")).strip().lower()
    market_id = str(row.get("market_id", "")).strip().lower()
    market_title = str(row.get("market_title", "")).strip().lower()
    team = str(row.get("team", "")).strip().lower()
    outcome = str(row.get("outcome", "")).strip().lower()

    if market_id:
        return f"{provider}|{market_id}|{outcome}"

    if team:
        return f"{provider}|{team}|{outcome}"

    return f"{provider}|{market_title}|{outcome}"


def compare_snapshots(
    previous: pd.DataFrame,
    current: pd.DataFrame,
) -> pd.DataFrame:
    comparison_timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    merged = previous.merge(
        current,
        on="comparison_key",
        how="outer",
        suffixes=("_previous", "_current"),
        indicator=True,
    )

    result = pd.DataFrame()
    result["comparison_timestamp"] = comparison_timestamp

    result["provider"] = merged["provider_current"].combine_first(
        merged["provider_previous"]
    )
    result["comparison_key"] = merged["comparison_key"]
    result["team"] = merged["team_current"].combine_first(merged["team_previous"])
    result["market_id"] = merged["market_id_current"].combine_first(
        merged["market_id_previous"]
    )
    result["market_title"] = merged["market_title_current"].combine_first(
        merged["market_title_previous"]
    )
    result["outcome"] = merged["outcome_current"].combine_first(
        merged["outcome_previous"]
    )

    result["status"] = merged["_merge"].map(
        {
            "both": "existing",
            "left_only": "removed",
            "right_only": "new",
        }
    )

    result["previous_probability"] = merged["probability_previous"].fillna(0.0)
    result["current_probability"] = merged["probability_current"].fillna(0.0)
    result["probability_change"] = (
        result["current_probability"] - result["previous_probability"]
    )
    result["probability_change_pp"] = result["probability_change"] * 100.0

    result["previous_volume"] = merged["volume_previous"].fillna(0.0)
    result["current_volume"] = merged["volume_current"].fillna(0.0)
    result["volume_change"] = result["current_volume"] - result["previous_volume"]

    result["previous_liquidity"] = merged["liquidity_previous"].fillna(0.0)
    result["current_liquidity"] = merged["liquidity_current"].fillna(0.0)
    result["liquidity_change"] = (
        result["current_liquidity"] - result["previous_liquidity"]
    )

    result["source_url"] = merged["source_url_current"].combine_first(
        merged["source_url_previous"]
    )

    result = result.sort_values(
        by=["probability_change_pp", "current_probability"],
        key=lambda series: series.abs() if series.name == "probability_change_pp" else series,
        ascending=[False, False],
    ).reset_index(drop=True)

    return result[OUTPUT_COLUMNS]


def main() -> None:
    args = parse_args()

    provider = str(args.provider).strip()
    snapshot_dir = Path(args.snapshot_dir)
    output_path = Path(args.output)

    previous_path, current_path = find_snapshot_pair(
        snapshot_dir=snapshot_dir,
        provider=provider,
        previous_path=args.previous,
        current_path=args.current,
    )

    print("Snapshot comparison utility")
    print(f"Previous snapshot: {previous_path}")
    print(f"Current snapshot:  {current_path}")
    print(f"Provider filter:   {provider or 'none'}")
    print("")

    previous_raw = pd.read_csv(previous_path)
    current_raw = pd.read_csv(current_path)

    previous = normalize_snapshot(previous_raw, provider)
    current = normalize_snapshot(current_raw, provider)

    comparison = compare_snapshots(previous, current)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    comparison.to_csv(output_path, index=False)

    print(f"Previous rows:   {len(previous)}")
    print(f"Current rows:    {len(current)}")
    print(f"Compared rows:   {len(comparison)}")
    print(f"Output written:  {output_path}")


if __name__ == "__main__":
    main()