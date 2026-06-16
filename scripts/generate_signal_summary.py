from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

DEFAULT_INPUT_PATH = ROOT / "data" / "processed" / "probability_deltas_latest.csv"
DEFAULT_OUTPUT_PATH = ROOT / "data" / "processed" / "signal_summary_latest.csv"


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
    "probability_change_pp",
    "probability_change_display",
    "direction",
    "current_volume",
    "volume_change",
    "current_liquidity",
    "liquidity_change",
    "signal_label",
    "signal_strength",
    "liquidity_label",
    "signal_reason",
    "source_url",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate transparent signal classifications from probability deltas.",
    )
    parser.add_argument(
        "--input",
        default=str(DEFAULT_INPUT_PATH),
        help="Input probability delta CSV path.",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_PATH),
        help="Output signal summary CSV path.",
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
        "--strong-threshold-pp",
        type=float,
        default=2.0,
        help="Absolute percentage-point move required for a strong signal.",
    )
    parser.add_argument(
        "--moderate-threshold-pp",
        type=float,
        default=0.75,
        help="Absolute percentage-point move required for a moderate signal.",
    )
    parser.add_argument(
        "--min-liquidity",
        type=float,
        default=1000.0,
        help="Minimum current liquidity before a move is treated as better supported.",
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


def ensure_numeric_column(dataframe: pd.DataFrame, column: str) -> pd.Series:
    if column not in dataframe.columns:
        return pd.Series([0.0] * len(dataframe), index=dataframe.index)

    return pd.to_numeric(
        dataframe[column],
        errors="coerce",
    ).fillna(0.0)


def classify_probability_signal(
    probability_change_pp: float,
    strong_threshold_pp: float,
    moderate_threshold_pp: float,
) -> tuple[str, str]:
    if probability_change_pp >= strong_threshold_pp:
        return "strong_positive_move", "strong"

    if probability_change_pp >= moderate_threshold_pp:
        return "moderate_positive_move", "moderate"

    if probability_change_pp <= -strong_threshold_pp:
        return "strong_negative_move", "strong"

    if probability_change_pp <= -moderate_threshold_pp:
        return "moderate_negative_move", "moderate"

    return "flat_no_signal", "none"


def classify_liquidity(
    current_liquidity: float,
    liquidity_change: float,
    min_liquidity: float,
) -> str:
    if current_liquidity <= 0:
        return "liquidity_unknown"

    if current_liquidity < min_liquidity:
        return "low_liquidity_noise"

    if liquidity_change > 0:
        return "rising_liquidity_support"

    if liquidity_change < 0:
        return "falling_liquidity"

    return "normal_liquidity"


def build_signal_reason(
    signal_label: str,
    liquidity_label: str,
    probability_change_pp: float,
    current_liquidity: float,
    liquidity_change: float,
) -> str:
    return (
        f"{signal_label}; "
        f"change={probability_change_pp:+.2f} pp; "
        f"{liquidity_label}; "
        f"current_liquidity={current_liquidity:.2f}; "
        f"liquidity_change={liquidity_change:+.2f}"
    )


def build_signal_summary(
    dataframe: pd.DataFrame,
    provider_filter: str,
    outcome_filter: str,
    strong_threshold_pp: float,
    moderate_threshold_pp: float,
    min_liquidity: float,
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

    working["previous_probability"] = ensure_numeric_column(
        working,
        "previous_probability",
    )
    working["current_probability"] = ensure_numeric_column(
        working,
        "current_probability",
    )
    working["probability_change_pp"] = ensure_numeric_column(
        working,
        "probability_change_pp",
    )
    working["current_volume"] = ensure_numeric_column(
        working,
        "current_volume",
    )
    working["volume_change"] = ensure_numeric_column(
        working,
        "volume_change",
    )
    working["current_liquidity"] = ensure_numeric_column(
        working,
        "current_liquidity",
    )
    working["liquidity_change"] = ensure_numeric_column(
        working,
        "liquidity_change",
    )

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    working["generated_at"] = generated_at

    signal_pairs = working["probability_change_pp"].apply(
        lambda value: classify_probability_signal(
            probability_change_pp=float(value),
            strong_threshold_pp=strong_threshold_pp,
            moderate_threshold_pp=moderate_threshold_pp,
        )
    )

    working["signal_label"] = signal_pairs.apply(lambda pair: pair[0])
    working["signal_strength"] = signal_pairs.apply(lambda pair: pair[1])

    working["liquidity_label"] = working.apply(
        lambda row: classify_liquidity(
            current_liquidity=float(row["current_liquidity"]),
            liquidity_change=float(row["liquidity_change"]),
            min_liquidity=min_liquidity,
        ),
        axis=1,
    )

    working["signal_reason"] = working.apply(
        lambda row: build_signal_reason(
            signal_label=str(row["signal_label"]),
            liquidity_label=str(row["liquidity_label"]),
            probability_change_pp=float(row["probability_change_pp"]),
            current_liquidity=float(row["current_liquidity"]),
            liquidity_change=float(row["liquidity_change"]),
        ),
        axis=1,
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
            "Run scripts/generate_probability_deltas.py first."
        )

    deltas = pd.read_csv(input_path)

    signal_summary = build_signal_summary(
        dataframe=deltas,
        provider_filter=str(args.provider).strip(),
        outcome_filter=str(args.outcome).strip(),
        strong_threshold_pp=float(args.strong_threshold_pp),
        moderate_threshold_pp=float(args.moderate_threshold_pp),
        min_liquidity=float(args.min_liquidity),
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    signal_summary.to_csv(output_path, index=False)

    print("Signal summary report")
    print(f"Input:                 {input_path}")
    print(f"Output:                {output_path}")
    print(f"Rows input:            {len(deltas)}")
    print(f"Rows output:           {len(signal_summary)}")
    print(f"Provider:              {args.provider or 'none'}")
    print(f"Outcome:               {args.outcome or 'none'}")
    print(f"Strong threshold pp:   {args.strong_threshold_pp}")
    print(f"Moderate threshold pp: {args.moderate_threshold_pp}")
    print(f"Min liquidity:         {args.min_liquidity}")


if __name__ == "__main__":
    main()