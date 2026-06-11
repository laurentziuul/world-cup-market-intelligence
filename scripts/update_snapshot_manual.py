from pathlib import Path
from datetime import datetime, timezone

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "data" / "manual" / "world_cup_markets.csv"
OUTPUT_DIR = ROOT / "data" / "processed"
OUTPUT_PATH = OUTPUT_DIR / "snapshot_latest.csv"


def main():
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
        "price_change_24h",
        "volume_change_24h",
        "narrative",
        "catalyst",
        "source_url",
        "notes",
    ]

    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df["snapshot_time_utc"] = datetime.now(timezone.utc).isoformat()
    df["provider"] = "manual_csv"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Created {OUTPUT_PATH}")
    print(f"Rows: {len(df)}")
    print("")
    print(df[["market_title", "outcome", "price", "narrative"]].to_string(index=False))


if __name__ == "__main__":
    main()