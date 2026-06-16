from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

DEFAULT_INPUT_PATH = ROOT / "data" / "processed" / "probability_deltas_latest.csv"
DEFAULT_OUTPUT_PATH = ROOT / "data" / "processed" / "top_movers_latest.csv"


OUTPUT_COLUMNS = [
    "generated_at",
    "category",
    "rank",
    "provider",
    "team",
    "market_id",
    "market_title",
    "outcome",
    "status",
    "previous_probability",
    "current_probability",
    "probability_change_pp",
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
        description="Generate top mover reports from probability delta output.",
    )
    parser.add_argument(
        "--input",
        default=str(DEFAULT_INPUT_PATH),
        help="Input probability delta CSV path.",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_PATH),
        help="Output top movers CSV path.",
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
        "--limit",
        type=int,
        default=10,
        help="Number of rows per mover category.",
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
            "Missing required columns in probability delta CSV: "
            + ", ".join(missing)
        )


def ensure_numeric(dataframe: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    working = dataframe.copy()

    for column in columns:
        working[column] = pd.to_numeric(
            working[column],
            errors="coerce",
        ).fillna(0.0)

    return working


def add_category(
    dataframe: pd.DataFrame,
    category: str,
    sort_column: str,
    ascending: bool,
    limit: int,
) -> pd.DataFrame:
    if dataframe.empty:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)

    selected = dataframe.sort_values(
        by=sort_column,
        ascending=ascending,
    ).head(limit).copy()

    selected.insert(0, "category", category)
    selected.insert(1, "rank", range(1, len(selected) + 1))

    return selected


def build_top_movers(
    dataframe: pd.DataFrame,
    provider_filter: str,
    outcome_filter: str,
    limit: int,
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
            "probability_change_pp",
            "probability_change_display",
            "direction",
            "source_url",
        ],
    )

    working = dataframe.copy()

    optional_numeric_columns = [
        "previous_volume",
        "current_volume",
        "volume_change",
        "previous_liquidity",
        "current_liquidity",
        "liquidity_change",
    ]

    for column in optional_numeric_columns:
        if column not in working.columns:
            working[column] = 0.0

    working = ensure_numeric(
        working,
        [
            "previous_probability",
            "current_probability",
            "probability_change_pp",
            "previous_volume",
            "current_volume",
            "volume_change",
            "previous_liquidity",
            "current_liquidity",
            "liquidity_change",
        ],
    )

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

    if min_abs_change_pp > 0:
        working = working[
            working["probability_change_pp"].abs() >= min_abs_change_pp
        ].copy()

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    working["generated_at"] = generated_at

    positive = working[working["probability_change_pp"] > 0].copy()
    negative = working[working["probability_change_pp"] < 0].copy()
    volume = working[working["volume_change"] != 0].copy()
    liquidity = working[working["liquidity_change"] != 0].copy()

    sections = [
        add_category(
            dataframe=positive,
            category="top_positive_probability_movers",
            sort_column="probability_change_pp",
            ascending=False,
            limit=limit,
        ),
        add_category(
            dataframe=negative,
            category="top_negative_probability_movers",
            sort_column="probability_change_pp",
            ascending=True,
            limit=limit,
        ),
        add_category(
            dataframe=volume,
            category="top_volume_movers",
            sort_column="volume_change",
            ascending=False,
            limit=limit,
        ),
        add_category(
            dataframe=liquidity,
            category="top_liquidity_movers",
            sort_column="liquidity_change",
            ascending=False,
            limit=limit,
        ),
    ]

    combined = pd.concat(sections, ignore_index=True)

    if combined.empty:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)

    return combined[OUTPUT_COLUMNS]


def main() -> None:
    args = parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        raise SystemExit(
            f"Input file does not exist: {input_path}\n"
            "Run scripts/generate_probability_deltas.py first."
        )

    deltas = pd.read_csv(input_path)

    top_movers = build_top_movers(
        dataframe=deltas,
        provider_filter=str(args.provider).strip(),
        outcome_filter=str(args.outcome).strip(),
        limit=int(args.limit),
        min_abs_change_pp=float(args.min_abs_change_pp),
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    top_movers.to_csv(output_path, index=False)

    print("Top movers report")
    print(f"Input:       {input_path}")
    print(f"Output:      {output_path}")
    print(f"Rows input:  {len(deltas)}")
    print(f"Rows output: {len(top_movers)}")
    print(f"Provider:    {args.provider or 'none'}")
    print(f"Outcome:     {args.outcome or 'none'}")
    print(f"Limit:       {args.limit}")
    print(f"Min abs pp:  {args.min_abs_change_pp}")


if __name__ == "__main__":
    main()