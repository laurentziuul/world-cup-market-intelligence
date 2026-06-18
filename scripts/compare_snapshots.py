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

    # Use the newest snapshot as "current"
    current = candidates[-1]

    # Try to find the snapshot closest to 24h before current (ideal for daily comparison).
    # Fall back to the oldest available snapshot for maximum delta window.
    try:
        current_mtime = current.stat().st_mtime
        target_mtime = current_mtime - 86400  # 24h ago
        best = min(
            candidates[:-1],
            key=lambda p: abs(p.stat().st_mtime - target_mtime),
        )
        previous = best
    except Exception:
        previous = candidates[0]

    return previous, current


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

    # NOTE: comparison_timestamp must be assigned AFTER at least one Series
    # column is set. Setting a scalar on an empty DataFrame produces NaN in all
    # rows because the index is not yet established (pandas 2.x behaviour).
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

    # Set scalar timestamp after rows exist so it broadcasts correctly.
    result["comparison_timestamp"] = comparison_timestamp

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

    previous_df = normalize_snapshot(previous_raw, provider)
    current_df = normalize_snapshot(current_raw, provider)

    if previous_df.empty or current_df.empty:
        raise SystemExit(
            f"One or both snapshots produced 0 rows after normalization.\n"
            f"Previous: {len(previous_df)} rows  Current: {len(current_df)} rows\n"
            "Check --provider filter and snapshot CSV content."
        )

    result = compare_snapshots(previous_df, current_df)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_path, index=False)

    status_counts = result["status"].value_counts()
    print(f"Rows in comparison: {len(result)}")
    for status_val, count in status_counts.items():
        print(f"  {status_val}: {count}")
    print(f"Output: {output_path}")
    print("")
    print("Snapshot comparison complete.")


if __name__ == "__main__":
    main()
