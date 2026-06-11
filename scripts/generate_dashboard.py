from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_PATH = ROOT / "data" / "processed" / "snapshot_latest.csv"
TEMPLATE_DIR = ROOT / "templates"
TEMPLATE_NAME = "dashboard.html.j2"
OUTPUT_DIR = ROOT / "dashboard"
OUTPUT_PATH = OUTPUT_DIR / "index.html"


def format_probability(value) -> str:
    try:
        value = float(value)
    except (TypeError, ValueError):
        return ""

    if value <= 1:
        return f"{value * 100:.1f}%"

    return f"{value:.1f}%"


def format_number(value) -> str:
    try:
        value = float(value)
    except (TypeError, ValueError):
        return "0"

    if value == 0:
        return "0"

    return f"{value:,.0f}"


def format_change(value) -> str:
    try:
        value = float(value)
    except (TypeError, ValueError):
        return "+0.0 pp"

    if abs(value) <= 1:
        return f"{value * 100:+.1f} pp"

    return f"{value:+.1f} pp"


def classify_signal(row: pd.Series) -> str:
    price = float(row.get("price_numeric", 0) or 0)
    volume = float(row.get("volume", 0) or 0)
    liquidity = float(row.get("liquidity", 0) or 0)
    price_change = abs(float(row.get("price_change_24h", 0) or 0))

    if volume > 0 and liquidity > 0 and price_change >= 0.03:
        return "Structural"

    if volume > 0 and liquidity > 0:
        return "Tactical"

    if price > 0:
        return "Speculative"

    return "Noise"


def normalize_snapshot(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    required_defaults = {
        "market_id": "",
        "market_title": "",
        "outcome": "",
        "price": 0,
        "volume": 0,
        "liquidity": 0,
        "price_change_24h": 0,
        "volume_change_24h": 0,
        "narrative": "",
        "catalyst": "",
        "source_url": "",
        "notes": "",
        "provider": "unknown",
        "snapshot_time_utc": "",
    }

    for column, default in required_defaults.items():
        if column not in df.columns:
            df[column] = default

    numeric_columns = [
        "price",
        "volume",
        "liquidity",
        "price_change_24h",
        "volume_change_24h",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

    df["market_display"] = df["market_title"].fillna("")
    df["price_numeric"] = df["price"]
    df["price_display"] = df["price"].apply(format_probability)
    df["volume_display"] = df["volume"].apply(format_number)
    df["liquidity_display"] = df["liquidity"].apply(format_number)
    df["price_change_display"] = df["price_change_24h"].apply(format_change)
    df["signal_class"] = df.apply(classify_signal, axis=1)

    df = df.sort_values("price_numeric", ascending=False)

    return df


def build_context(df: pd.DataFrame) -> dict:
    df = normalize_snapshot(df)

    rows = df.to_dict("records")

    provider = str(df["provider"].iloc[0]) if len(df) else "unknown"
    snapshot_time = str(df["snapshot_time_utc"].iloc[0]) if len(df) else ""

    total_volume = df["volume"].sum()
    total_liquidity = df["liquidity"].sum()

    leading = rows[0] if rows else {}

    if total_volume == 0 and total_liquidity == 0:
        liquidity_note = (
            "Volume and liquidity are currently zero because the dashboard is using "
            "the manual CSV provider. Treat this as a structural test, not a live liquidity signal."
        )
    else:
        liquidity_note = (
            "The snapshot includes non-zero volume or liquidity. These fields should be "
            "used to separate stronger market-structure signals from narrative-only noise."
        )

    red_team_notes = [
        "Manual data may not reflect live market prices.",
        "Zero liquidity means the current snapshot should not be interpreted as a tradable signal.",
        "High implied probability can reflect reputation, public bias or stale assumptions.",
        "Without historical snapshots, static prices cannot yet be separated from real probability moves.",
        "Without multiple providers, there is no cross-market confirmation.",
    ]

    return {
        "provider": provider,
        "row_count": len(df),
        "snapshot_time": snapshot_time,
        "snapshot_path": str(SNAPSHOT_PATH.relative_to(ROOT)),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_volume_display": format_number(total_volume),
        "total_liquidity_display": format_number(total_liquidity),
        "leading_outcome": leading.get("outcome", "N/A"),
        "leading_price": leading.get("price_display", "N/A"),
        "liquidity_note": liquidity_note,
        "red_team_notes": red_team_notes,
        "rows": rows,
    }


def render_dashboard(context: dict) -> str:
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(TEMPLATE_NAME)
    return template.render(**context)


def main() -> None:
    if not SNAPSHOT_PATH.exists():
        raise FileNotFoundError(
            f"Snapshot not found: {SNAPSHOT_PATH}\n"
            "Run this first:\n"
            "python scripts/update_snapshot_manual.py"
        )

    df = pd.read_csv(SNAPSHOT_PATH)
    context = build_context(df)
    html = render_dashboard(context)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(html, encoding="utf-8")

    print(f"Dashboard saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()