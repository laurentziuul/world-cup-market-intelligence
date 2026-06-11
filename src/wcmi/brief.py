from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

from wcmi.config import settings


def load_latest_snapshot(path: Path | None = None) -> pd.DataFrame:
    snapshot_path = path or settings.data_processed_dir / "snapshot_latest.csv"
    if not snapshot_path.exists():
        raise FileNotFoundError(f"Snapshot not found: {snapshot_path}")
    return pd.read_csv(snapshot_path)


def _first_existing_column(df: pd.DataFrame, candidates: list[str], fallback: str) -> str:
    for column in candidates:
        if column in df.columns:
            return column
    return fallback


def _format_probability(value) -> str:
    try:
        value = float(value)
    except (TypeError, ValueError):
        return ""

    if value <= 1:
        return f"{value * 100:.1f}%"
    return f"{value:.1f}%"


def _format_number(value) -> str:
    try:
        value = float(value)
    except (TypeError, ValueError):
        return ""

    if value == 0:
        return "0"

    return f"{value:,.0f}"


def _format_change(value) -> str:
    try:
        value = float(value)
    except (TypeError, ValueError):
        return "0.0 pp"

    if abs(value) <= 1:
        return f"{value * 100:+.1f} pp"

    return f"{value:+.1f} pp"


def _normalize_snapshot(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    market_col = _first_existing_column(df, ["market_title", "question", "market"], "market_title")
    price_col = _first_existing_column(df, ["price", "current_price"], "price")

    if market_col not in df.columns:
        df["market_title"] = ""
        market_col = "market_title"

    if price_col not in df.columns:
        df["price"] = 0.0
        price_col = "price"

    for column in ["price", "current_price", "volume", "liquidity", "price_change_24h", "volume_change_24h"]:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

    df["market_display"] = df[market_col].fillna("")
    df["price_numeric"] = pd.to_numeric(df[price_col], errors="coerce").fillna(0)
    df["price_display"] = df["price_numeric"].apply(_format_probability)

    if "volume" not in df.columns:
        df["volume"] = 0

    if "liquidity" not in df.columns:
        df["liquidity"] = 0

    if "price_change_24h" not in df.columns:
        df["price_change_24h"] = 0

    if "volume_change_24h" not in df.columns:
        df["volume_change_24h"] = 0

    if "narrative" not in df.columns:
        df["narrative"] = ""

    if "catalyst" not in df.columns:
        df["catalyst"] = ""

    if "provider" not in df.columns:
        df["provider"] = "unknown"

    df["volume_display"] = df["volume"].apply(_format_number)
    df["liquidity_display"] = df["liquidity"].apply(_format_number)
    df["price_change_display"] = df["price_change_24h"].apply(_format_change)

    return df


def build_brief_context(df: pd.DataFrame) -> dict:
    df = _normalize_snapshot(df)

    top_probability = (
        df.sort_values("price_numeric", ascending=False)
        .head(10)
        .fillna("")
        .to_dict("records")
    )

    top_volume = (
        df.sort_values("volume", ascending=False)
        .head(5)
        .fillna("")
        .to_dict("records")
    )

    top_liquidity = (
        df.sort_values("liquidity", ascending=False)
        .head(5)
        .fillna("")
        .to_dict("records")
    )

    biggest_move_row = (
        df.assign(abs_move=df["price_change_24h"].abs())
        .sort_values("abs_move", ascending=False)
        .head(1)
    )

    biggest_move = biggest_move_row.iloc[0].to_dict() if not biggest_move_row.empty else {}

    crowded_trade_row = df.sort_values("price_numeric", ascending=False).head(1)
    crowded_trade = crowded_trade_row.iloc[0].to_dict() if not crowded_trade_row.empty else {}

    provider = df["provider"].iloc[0] if "provider" in df.columns and len(df) else "unknown"

    has_real_liquidity = bool((df["volume"].sum() > 0) or (df["liquidity"].sum() > 0))

    if has_real_liquidity:
        liquidity_note = "The dataset includes non-zero volume/liquidity fields. These should be treated as stronger market-structure inputs than narrative notes."
    else:
        liquidity_note = "Volume and liquidity are currently zero because this snapshot comes from the manual CSV provider. Treat this as a structural test, not a live liquidity signal."

    if crowded_trade:
        bottom_line = (
            f"The current manual snapshot shows {crowded_trade.get('outcome', 'the leading outcome')} "
            f"as one of the highest-priced outcomes at {crowded_trade.get('price_display', '')}. "
            "Because this is a manual v0 dataset, the main value is pipeline validation: data intake, snapshot normalization, and brief generation now work end-to-end."
        )
    else:
        bottom_line = "The current snapshot is empty. Add rows to the manual CSV provider before interpreting market structure."

    return {
        "brief_date": date.today().isoformat(),
        "provider": provider,
        "row_count": len(df),
        "top_probability": top_probability,
        "top_volume": top_volume,
        "top_liquidity": top_liquidity,
        "biggest_move": biggest_move,
        "crowded_trade": crowded_trade,
        "liquidity_note": liquidity_note,
        "bottom_line": bottom_line,
        "manual_notes": [
            "Manual CSV provider is the default v0 data source.",
            "External APIs are optional providers, not hard dependencies.",
            "Classify each signal as structural / tactical / speculative.",
            "Red-team the strongest signal before publishing.",
        ],
    }


def render_brief(context: dict, template_name: str = "daily_brief.md.j2") -> str:
    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape(default_for_string=False),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(template_name)
    return template.render(**context)


def save_brief(markdown: str, output_dir: Path | None = None, brief_date: str | None = None) -> Path:
    out_dir = output_dir or settings.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    slug_date = brief_date or date.today().isoformat()
    path = out_dir / f"{slug_date}-world-cup-market-brief.md"
    path.write_text(markdown, encoding="utf-8")
    return path