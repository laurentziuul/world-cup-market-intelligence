from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from wcmi.providers.manual_csv import ManualCsvProvider


ROOT = Path(__file__).resolve().parents[1]

OUTPUT_DIR = ROOT / "data" / "processed"
LATEST_PATH = OUTPUT_DIR / "snapshot_latest.csv"
SNAPSHOT_ARCHIVE_DIR = OUTPUT_DIR / "snapshots"


PROVIDERS = {
    "manual_csv": ManualCsvProvider,
}


def load_provider(provider_name: str):
    if provider_name not in PROVIDERS:
        available = ", ".join(sorted(PROVIDERS))
        raise ValueError(
            f"Unknown provider: {provider_name}\n"
            f"Available providers: {available}"
        )

    provider_class = PROVIDERS[provider_name]
    return provider_class()


def normalize_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    numeric_columns = [
        "price",
        "volume",
        "liquidity",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

    return df


def load_previous_snapshot() -> pd.DataFrame | None:
    if not LATEST_PATH.exists():
        return None

    try:
        previous = pd.read_csv(LATEST_PATH)
    except Exception:
        return None

    if previous.empty:
        return None

    return previous


def calculate_changes(current: pd.DataFrame, previous: pd.DataFrame | None) -> pd.DataFrame:
    current = current.copy()

    current["price_change_24h"] = 0.0
    current["volume_change_24h"] = 0.0
    current["liquidity_change_24h"] = 0.0

    if previous is None or previous.empty:
        return current

    previous = previous.copy()

    required_previous_columns = [
        "market_id",
        "outcome",
        "price",
        "volume",
        "liquidity",
    ]

    missing_previous = [column for column in required_previous_columns if column not in previous.columns]

    if missing_previous:
        return current

    previous = normalize_numeric_columns(previous)

    previous_small = previous[
        [
            "market_id",
            "outcome",
            "price",
            "volume",
            "liquidity",
        ]
    ].rename(
        columns={
            "price": "previous_price",
            "volume": "previous_volume",
            "liquidity": "previous_liquidity",
        }
    )

    merged = current.merge(
        previous_small,
        on=[
            "market_id",
            "outcome",
        ],
        how="left",
    )

    merged["previous_price"] = merged["previous_price"].fillna(merged["price"])
    merged["previous_volume"] = merged["previous_volume"].fillna(merged["volume"])
    merged["previous_liquidity"] = merged["previous_liquidity"].fillna(merged["liquidity"])

    merged["price_change_24h"] = merged["price"] - merged["previous_price"]
    merged["volume_change_24h"] = merged["volume"] - merged["previous_volume"]
    merged["liquidity_change_24h"] = merged["liquidity"] - merged["previous_liquidity"]

    merged = merged.drop(
        columns=[
            "previous_price",
            "previous_volume",
            "previous_liquidity",
        ]
    )

    return merged


def add_metadata(df: pd.DataFrame, snapshot_time: datetime, provider_name: str) -> pd.DataFrame:
    df = df.copy()

    df["snapshot_time_utc"] = snapshot_time.isoformat()
    df["snapshot_date_utc"] = snapshot_time.date().isoformat()
    df["provider"] = provider_name

    return df


def build_archive_filename(snapshot_time: datetime, provider_name: str) -> str:
    timestamp = snapshot_time.strftime("%Y-%m-%dT%H-%M-%SZ")
    return f"{timestamp}-{provider_name}.csv"


def write_outputs(df: pd.DataFrame, snapshot_time: datetime, provider_name: str) -> tuple[Path, Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    archive_filename = build_archive_filename(snapshot_time, provider_name)
    archive_path = SNAPSHOT_ARCHIVE_DIR / archive_filename

    df.to_csv(LATEST_PATH, index=False)
    df.to_csv(archive_path, index=False)

    return LATEST_PATH, archive_path


def update_snapshot(provider_name: str) -> tuple[pd.DataFrame, Path, Path]:
    snapshot_time = datetime.now(timezone.utc)

    provider = load_provider(provider_name)

    current = provider.load()
    current = normalize_numeric_columns(current)

    previous = load_previous_snapshot()
    current = calculate_changes(current, previous)
    current = add_metadata(current, snapshot_time, provider_name)

    latest_path, archive_path = write_outputs(current, snapshot_time, provider_name)

    return current, latest_path, archive_path


def print_snapshot_summary(df: pd.DataFrame, latest_path: Path, archive_path: Path) -> None:
    print(f"Created latest snapshot: {latest_path}")
    print(f"Archived timestamped snapshot: {archive_path}")
    print(f"Rows: {len(df)}")
    print("")

    display_columns = [
        "market_title",
        "outcome",
        "price",
        "price_change_24h",
        "volume",
        "liquidity",
        "provider",
        "narrative",
    ]

    print(df[display_columns].to_string(index=False))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Update normalized market snapshot from a provider."
    )

    parser.add_argument(
        "--provider",
        default="manual_csv",
        choices=sorted(PROVIDERS.keys()),
        help="Market data provider to use.",
    )

    return parser.parse_args()


def main(provider_name: str | None = None) -> None:
    if provider_name is None:
        args = parse_args()
        provider_name = args.provider

    df, latest_path, archive_path = update_snapshot(provider_name)
    print_snapshot_summary(df, latest_path, archive_path)


if __name__ == "__main__":
    main()