from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape


ROOT = Path(__file__).resolve().parents[1]

SNAPSHOT_PATH = ROOT / "data" / "processed" / "snapshot_latest.csv"
TRENDS_PATH = ROOT / "data" / "processed" / "trends_latest.csv"

TEMPLATE_DIR = ROOT / "templates"
TEMPLATE_NAME = "dashboard.html.j2"

OUTPUT_DIR = ROOT / "docs" / "dashboard"
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
        "liquidity_change_24h": 0,
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
        "liquidity_change_24h",
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


def build_movers_context(df: pd.DataFrame) -> dict:
    positive_movers_df = df[df["price_change_24h"] > 0].sort_values(
        "price_change_24h",
        ascending=False,
    )

    negative_movers_df = df[df["price_change_24h"] < 0].sort_values(
        "price_change_24h",
        ascending=True,
    )

    top_positive_movers = positive_movers_df.head(5).to_dict("records")
    top_negative_movers = negative_movers_df.head(5).to_dict("records")

    active_movers_count = int((df["price_change_24h"].abs() > 0).sum())
    static_markets_count = int((df["price_change_24h"].abs() == 0).sum())

    biggest_up_move = (
        f"{top_positive_movers[0].get('outcome', 'N/A')} "
        f"{top_positive_movers[0].get('price_change_display', '')}"
        if top_positive_movers
        else "N/A"
    )

    biggest_down_move = (
        f"{top_negative_movers[0].get('outcome', 'N/A')} "
        f"{top_negative_movers[0].get('price_change_display', '')}"
        if top_negative_movers
        else "N/A"
    )

    return {
        "top_positive_movers": top_positive_movers,
        "top_negative_movers": top_negative_movers,
        "active_movers_count": active_movers_count,
        "static_markets_count": static_markets_count,
        "biggest_up_move": biggest_up_move,
        "biggest_down_move": biggest_down_move,
    }


def load_trends() -> pd.DataFrame | None:
    if not TRENDS_PATH.exists():
        return None

    try:
        trends = pd.read_csv(TRENDS_PATH)
    except Exception:
        return None

    if trends.empty:
        return None

    return trends


def normalize_trends(trends: pd.DataFrame | None) -> pd.DataFrame:
    if trends is None or trends.empty:
        return pd.DataFrame()

    trends = trends.copy()

    required_defaults = {
        "market_id": "",
        "market_title": "",
        "outcome": "",
        "first_price": 0,
        "latest_price": 0,
        "total_change": 0,
        "max_price": 0,
        "min_price": 0,
        "observations": 0,
        "trend_direction": "flat",
        "trend_quality": "weak",
        "latest_narrative": "",
        "latest_catalyst": "",
    }

    for column, default in required_defaults.items():
        if column not in trends.columns:
            trends[column] = default

    numeric_columns = [
        "first_price",
        "latest_price",
        "total_change",
        "max_price",
        "min_price",
        "observations",
    ]

    for column in numeric_columns:
        trends[column] = pd.to_numeric(trends[column], errors="coerce").fillna(0)

    trends["first_price_display"] = trends["first_price"].apply(format_probability)
    trends["latest_price_display"] = trends["latest_price"].apply(format_probability)
    trends["total_change_display"] = trends["total_change"].apply(format_change)
    trends["max_price_display"] = trends["max_price"].apply(format_probability)
    trends["min_price_display"] = trends["min_price"].apply(format_probability)

    return trends


def build_trends_context() -> dict:
    trends = normalize_trends(load_trends())

    if trends.empty:
        return {
            "has_trends": False,
            "trend_rows": [],
            "top_uptrends": [],
            "top_downtrends": [],
            "tracked_trends_count": 0,
            "strong_trends_count": 0,
            "emerging_trends_count": 0,
            "weak_trends_count": 0,
            "strongest_uptrend": "N/A",
            "strongest_downtrend": "N/A",
            "max_observations": 0,
        }

    top_uptrends_df = trends[trends["total_change"] > 0].sort_values(
        "total_change",
        ascending=False,
    )

    top_downtrends_df = trends[trends["total_change"] < 0].sort_values(
        "total_change",
        ascending=True,
    )

    top_uptrends = top_uptrends_df.head(5).to_dict("records")
    top_downtrends = top_downtrends_df.head(5).to_dict("records")

    strongest_uptrend = (
        f"{top_uptrends[0].get('outcome', 'N/A')} "
        f"{top_uptrends[0].get('total_change_display', '')}"
        if top_uptrends
        else "N/A"
    )

    strongest_downtrend = (
        f"{top_downtrends[0].get('outcome', 'N/A')} "
        f"{top_downtrends[0].get('total_change_display', '')}"
        if top_downtrends
        else "N/A"
    )

    strong_trends_count = int((trends["trend_quality"] == "strong").sum())
    emerging_trends_count = int((trends["trend_quality"] == "emerging").sum())
    weak_trends_count = int((trends["trend_quality"] == "weak").sum())

    trends_sorted = trends.sort_values(
        ["trend_quality", "total_change"],
        ascending=[True, False],
    )

    return {
        "has_trends": True,
        "trend_rows": trends_sorted.to_dict("records"),
        "top_uptrends": top_uptrends,
        "top_downtrends": top_downtrends,
        "tracked_trends_count": len(trends),
        "strong_trends_count": strong_trends_count,
        "emerging_trends_count": emerging_trends_count,
        "weak_trends_count": weak_trends_count,
        "strongest_uptrend": strongest_uptrend,
        "strongest_downtrend": strongest_downtrend,
        "max_observations": int(trends["observations"].max()),
    }


def build_context(df: pd.DataFrame) -> dict:
    df = normalize_snapshot(df)

    rows = df.to_dict("records")
    movers_context = build_movers_context(df)
    trends_context = build_trends_context()

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
        "Without enough historical snapshots, static prices cannot yet be separated from persistent trends.",
        "Without multiple providers, there is no cross-market confirmation.",
    ]

    context = {
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

    context.update(movers_context)
    context.update(trends_context)

    return context


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