from pathlib import Path
from datetime import datetime, timezone

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

INPUT_PATH = ROOT / "data" / "manual" / "world_cup_markets.csv"

OUTPUT_DIR = ROOT / "data" / "processed"
LATEST_PATH = OUTPUT_DIR / "snapshot_latest.csv"

SNAPSHOT_ARCHIVE_DIR = OUTPUT_DIR / "snapshots"


def load_manual_data() -> pd.DataFrame:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Manual input file not found: {INPUT_PATH}\n"
            "Create data/manual/world_cup_markets.csv first."
        )

    df = pd.read_csv(INPUT_PATH)

    required_columns = [
        "market_id",
        "market_title",
        "outcome",
        "price",
        "volume",
        "liquidity",
        "narrative",
        "catalyst",
        "source_url",
        "notes",
    ]

    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return df


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

    missing_previous = [col for col in required_previous_columns if col not in previous.columns]
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
        on=["market_id", "outcome"],
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


def add_metadata(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    now = datetime.now(timezone.utc)

    df["snapshot_time_utc"] = now.isoformat()
    df["snapshot_date_utc"] = now.date().isoformat()
    df["provider"] = "manual_csv"

    return df


def write_outputs(df: pd.DataFrame) -> tuple[Path, Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    snapshot_date = df["snapshot_date_utc"].iloc[0]
    archive_path = SNAPSHOT_ARCHIVE_DIR / f"{snapshot_date}.csv"

    df.to_csv(LATEST_PATH, index=False)
    df.to_csv(archive_path, index=False)

    return LATEST_PATH, archive_path


def main():
    current = load_manual_data()
    current = normalize_numeric_columns(current)

    previous = load_previous_snapshot()
    current = calculate_changes(current, previous)
    current = add_metadata(current)

    latest_path, archive_path = write_outputs(current)

    print(f"Created latest snapshot: {latest_path}")
    print(f"Archived daily snapshot: {archive_path}")
    print(f"Rows: {len(current)}")
    print("")

    display_columns = [
        "market_title",
        "outcome",
        "price",
        "price_change_24h",
        "volume",
        "liquidity",
        "narrative",
    ]

    print(current[display_columns].to_string(index=False))


if __name__ == "__main__":
    main()