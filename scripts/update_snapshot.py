from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from wcmi.config import settings
from wcmi.polymarket import fetch_world_cup_snapshots


def main() -> None:
    settings.data_raw_dir.mkdir(parents=True, exist_ok=True)
    settings.data_processed_dir.mkdir(parents=True, exist_ok=True)

    snapshots = fetch_world_cup_snapshots(query=settings.event_query, limit=100)
    rows = [s.model_dump(mode="json", exclude={"raw"}) for s in snapshots]
    raw_rows = [s.model_dump(mode="json") for s in snapshots]

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    raw_path = settings.data_raw_dir / f"polymarket_world_cup_{ts}.json"
    processed_path = settings.data_processed_dir / f"snapshot_{ts}.csv"
    latest_path = settings.data_processed_dir / "snapshot_latest.csv"

    raw_path.write_text(json.dumps(raw_rows, indent=2), encoding="utf-8")
    df = pd.DataFrame(rows)
    df.to_csv(processed_path, index=False)
    df.to_csv(latest_path, index=False)

    print(f"Fetched {len(df)} market outcome rows")
    print(f"Raw: {raw_path}")
    print(f"Processed: {processed_path}")
    print(f"Latest: {latest_path}")


if __name__ == "__main__":
    main()
