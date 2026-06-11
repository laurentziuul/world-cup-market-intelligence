from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

SNAPSHOT_ARCHIVE_DIR = ROOT / "data" / "processed" / "snapshots"
OUTPUT_PATH = ROOT / "data" / "processed" / "trends_latest.csv"


def format_probability(value) -> str:
    try:
        value = float(value)
    except (TypeError, ValueError):
        return ""

    if value <= 1:
        return f"{value * 100:.1f}%"

    return f"{value:.1f}%"


def format_change(value) -> str:
    try:
        value = float(value)
    except (TypeError, ValueError):
        return "+0.0 pp"

    if abs(value) <= 1:
        return f"{value * 100:+.1f} pp"

    return f"{value:+.1f} pp"


def list_snapshot_files() -> list[Path]:
    if not SNAPSHOT_ARCHIVE_DIR.exists():
        raise FileNotFoundError(
            f"Snapshot archive folder not found: {SNAPSHOT_ARCHIVE_DIR}\n"
            "Run this first:\n"
            "python scripts/update_snapshot_manual.py"
        )

    files = sorted(
        path
        for path in SNAPSHOT_ARCHIVE_DIR.glob("*.csv")
        if path.is_file()
    )

    if not files:
        raise FileNotFoundError(
            f"No snapshot CSV files found in: {SNAPSHOT_ARCHIVE_DIR}\n"
            "Run this first:\n"
            "python scripts/update_snapshot_manual.py"
        )

    return files


def load_snapshots() -> pd.DataFrame:
    frames = []

    for path in list_snapshot_files():
        df = pd.read_csv(path)
        df["snapshot_file"] = path.name
        frames.append(df)

    combined = pd.concat(frames, ignore_index=True)

    required_columns = [
        "market_id",
        "market_title",
        "outcome",
        "price",
        "volume",
        "liquidity",
        "narrative",
        "catalyst",
        "provider",
        "snapshot_time_utc",
    ]

    for column in required_columns:
        if column not in combined.columns:
            combined[column] = ""

    numeric_columns = [
        "price",
        "volume",
        "liquidity",
    ]

    for column in numeric_columns:
        combined[column] = pd.to_numeric(combined[column], errors="coerce").fillna(0)

    combined["snapshot_time_parsed"] = pd.to_datetime(
        combined["snapshot_time_utc"],
        errors="coerce",
        utc=True,
    )

    combined = combined.dropna(subset=["snapshot_time_parsed"])

    if combined.empty:
        raise ValueError(
            "Snapshots were found, but none had a valid snapshot_time_utc field."
        )

    combined = combined.sort_values(
        [
            "market_id",
            "outcome",
            "snapshot_time_parsed",
        ]
    )

    return combined


def classify_trend(total_change: float, observations: int) -> tuple[str, str]:
    abs_change = abs(total_change)

    if total_change > 0.001:
        direction = "up"
    elif total_change < -0.001:
        direction = "down"
    else:
        direction = "flat"

    if observations < 2:
        quality = "weak"
    elif abs_change >= 0.03 and observations >= 3:
        quality = "strong"
    elif abs_change >= 0.01:
        quality = "emerging"
    else:
        quality = "weak"

    return direction, quality


def build_trends(df: pd.DataFrame) -> pd.DataFrame:
    rows = []

    group_columns = [
        "market_id",
        "outcome",
    ]

    for (market_id, outcome), group in df.groupby(group_columns):
        group = group.sort_values("snapshot_time_parsed")

        first = group.iloc[0]
        latest = group.iloc[-1]

        first_price = float(first["price"])
        latest_price = float(latest["price"])
        total_change = latest_price - first_price

        observations = int(len(group))
        trend_direction, trend_quality = classify_trend(total_change, observations)

        row = {
            "market_id": market_id,
            "market_title": latest.get("market_title", ""),
            "outcome": outcome,
            "first_price": first_price,
            "latest_price": latest_price,
            "total_change": total_change,
            "max_price": float(group["price"].max()),
            "min_price": float(group["price"].min()),
            "observations": observations,
            "first_snapshot_time_utc": str(first["snapshot_time_utc"]),
            "latest_snapshot_time_utc": str(latest["snapshot_time_utc"]),
            "latest_narrative": latest.get("narrative", ""),
            "latest_catalyst": latest.get("catalyst", ""),
            "provider": latest.get("provider", "unknown"),
            "trend_direction": trend_direction,
            "trend_quality": trend_quality,
        }

        rows.append(row)

    trends = pd.DataFrame(rows)

    if trends.empty:
        return trends

    trends["first_price_display"] = trends["first_price"].apply(format_probability)
    trends["latest_price_display"] = trends["latest_price"].apply(format_probability)
    trends["total_change_display"] = trends["total_change"].apply(format_change)
    trends["max_price_display"] = trends["max_price"].apply(format_probability)
    trends["min_price_display"] = trends["min_price"].apply(format_probability)

    trends = trends.sort_values(
        [
            "trend_quality",
            "total_change",
        ],
        ascending=[
            True,
            False,
        ],
    )

    quality_rank = {
        "strong": 0,
        "emerging": 1,
        "weak": 2,
    }

    trends["trend_quality_rank"] = trends["trend_quality"].map(quality_rank).fillna(9)

    trends = trends.sort_values(
        [
            "trend_quality_rank",
            "total_change",
        ],
        ascending=[
            True,
            False,
        ],
    ).drop(columns=["trend_quality_rank"])

    return trends


def main() -> None:
    snapshots = load_snapshots()
    trends = build_trends(snapshots)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    trends.to_csv(OUTPUT_PATH, index=False)

    print(f"Trend file saved: {OUTPUT_PATH}")
    print(f"Snapshot files analyzed: {len(list_snapshot_files())}")
    print(f"Trend rows: {len(trends)}")
    print("")

    if trends.empty:
        print("No trends generated.")
        return

    display_columns = [
        "market_title",
        "outcome",
        "first_price_display",
        "latest_price_display",
        "total_change_display",
        "observations",
        "trend_direction",
        "trend_quality",
    ]

    print(trends[display_columns].to_string(index=False))


if __name__ == "__main__":
    main()