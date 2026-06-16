from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

DEFAULT_INPUT_PATH = ROOT / "data" / "processed" / "snapshot_comparison_latest.csv"
DEFAULT_OUTPUT_PATH = ROOT / "data" / "processed" / "probability_deltas_latest.csv"


OUTPUT_COLUMNS = [
    "generated_at",
    "provider",
    "team",
    "market_id",
    "market_title",
    "outcome",
    "status",
    "previous_probability",
    "current_probability",
    "probability_change",
    "probability_change_pp",
    "previous_probability_display",
    "current_probability_display",
    "probability_change_display",
    "direction",
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
        description="Generate a clean probability delta report from snapshot comparison output.",
    )
    parser.add_argument(
        "--input",
        default=str(DEFAULT_INPUT_PATH),
        help="Input snapshot comparison CSV path.",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_PATH),
        help="Output probability delta CSV path.",
    )
    parser.add_argument(
        "--provider",
        default="",
        help="Optional provider filter, for example: manual_csv or polymarket.",
    )
    parser.add_argument(
        "--outcome",
        default="",
        help="Optional outcome filter, for example: Yes.",
    )
    parser.add_argument(
        "--status",
        default="",
        help="Optional status filter: existing, new or removed.",
    )
    parser.add_argument(
        "--min-abs-change-pp",
        type=float,
        default=0.0,
        help="Minimum absolute probability change in percentage points.",
    )
    return parser.parse_args()


def require_columns(dataframe: pd.DataFrame, columns: list[str]) -> None:
    missing = [
        column
        for column in columns
        if column not in dataframe.columns
    ]

    if missing:
        raise SystemExit(
            "Missing required columns in comparison CSV: "
            + ", ".join(missing)
        )


def ensure_numeric_column(dataframe: pd.DataFrame, column: str) -> pd.Series:
    if column not in dataframe.columns:
        return pd.Series([0.0] * len(dataframe), index=dataframe.index)

    return pd.to_numeric(
        dataframe[column],
        errors="coerce",
    ).fillna(0.0)


def format_probability(value: float) -> str:
    return f"{value * 100:.2f}%"


def format_change_pp(value: float) -> str:
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.2f} pp"


def classify_direction(value: float) -> str:
    if value > 0:
        return "up"

    if value < 0:
        return "down"

    return "flat"


def build_probability_deltas(
    dataframe: pd.DataFrame,
    provider_filter: str,
    outcome_filter: str,
    status_filter: str,
    min_abs_change_pp: float,
) -> pd.DataFrame:
    require_columns(
        dataframe,
        [
            "provider",
            "team",
            "market_id",
            "market_title",
            "outcome",
            "status",
            "previous_probability",
            "current_probability",
            "probability_change",
            "probability_change_pp",
            "source_url",
        ],
    )

    working = dataframe.copy()

    if provider_filter:
        working = working[
            working["provider"].astype(str).str.lower()
            == provider_filter.lower()
        ].copy()

    if outcome_filter:
        working = working[
            working["outcome"].astype(str).str.lower()
            == outcome_filter.lower()
        ].copy()

    if status_filter:
        working = working[
            working["status"].astype(str).str.lower()
            == status_filter.lower()
        ].copy()

    working["previous_probability"] = ensure_numeric_column(
        working,
        "previous_probability",
    )
    working["current_probability"] = ensure_numeric_column(
        working,
        "current_probability",
    )
    working["probability_change"] = ensure_numeric_column(
        working,
        "probability_change",
    )
    working["probability_change_pp"] = ensure_numeric_column(
        working,
        "probability_change_pp",
    )

    working["previous_volume"] = ensure_numeric_column(
        working,
        "previous_volume",
    )
    working["current_volume"] = ensure_numeric_column(
        working,
        "current_volume",
    )
    working["volume_change"] = ensure_numeric_column(
        working,
        "volume_change",
    )

    working["previous_liquidity"] = ensure_numeric_column(
        working,
        "previous_liquidity",
    )
    working["current_liquidity"] = ensure_numeric_column(
        working,
        "current_liquidity",
    )
    working["liquidity_change"] = ensure_numeric_column(
        working,
        "liquidity_change",
    )

    if min_abs_change_pp > 0:
        working = working[
            working["probability_change_pp"].abs() >= min_abs_change_pp
        ].copy()

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    working["generated_at"] = generated_at
    working["previous_probability_display"] = working[
        "previous_probability"
    ].apply(format_probability)
    working["current_probability_display"] = working[
        "current_probability"
    ].apply(format_probability)
    working["probability_change_display"] = working[
        "probability_change_pp"
    ].apply(format_change_pp)
    working["direction"] = working["probability_change_pp"].apply(
        classify_direction
    )

    working = working.sort_values(
        by=["probability_change_pp", "current_probability"],
        key=lambda series: (
            series.abs()
            if series.name == "probability_change_pp"
            else series
        ),
        ascending=[False, False],
    ).reset_index(drop=True)

    return working[OUTPUT_COLUMNS]


def main() -> None:
    args = parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        raise SystemExit(
            f"Input file does not exist: {input_path}\n"
            "Run scripts/compare_snapshots.py first."
        )

    comparison = pd.read_csv(input_path)

    deltas = build_probability_deltas(
        dataframe=comparison,
        provider_filter=str(args.provider).strip(),
        outcome_filter=str(args.outcome).strip(),
        status_filter=str(args.status).strip(),
        min_abs_change_pp=float(args.min_abs_change_pp),
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    deltas.to_csv(output_path, index=False)

    print("Probability delta report")
    print(f"Input:       {input_path}")
    print(f"Output:      {output_path}")
    print(f"Rows input:  {len(comparison)}")
    print(f"Rows output: {len(deltas)}")
    print(f"Provider:    {args.provider or 'none'}")
    print(f"Outcome:     {args.outcome or 'none'}")
    print(f"Status:      {args.status or 'none'}")
    print(f"Min abs pp:  {args.min_abs_change_pp}")


if __name__ == "__main__":
    main()