from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

DEFAULT_SIGNAL_SUMMARY_PATH = ROOT / "data" / "processed" / "signal_summary_latest.csv"
DEFAULT_CATALYST_MATCHES_PATH = ROOT / "data" / "processed" / "catalyst_matches_latest.csv"
DEFAULT_OUTPUT_PATH = ROOT / "data" / "processed" / "team_intelligence_latest.csv"


OUTPUT_COLUMNS = [
    "team",
    "provider",
    "total_signals",
    "positive_signals",
    "negative_signals",
    "flat_signals",
    "matched_catalysts",
    "unmatched_signals",
    "high_confidence_catalysts",
    "medium_confidence_catalysts",
    "low_confidence_catalysts",
    "strongest_signal",
    "latest_signal_date",
    "latest_catalyst_date",
    "summary_label",
    "review_priority",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate team-level intelligence summary from signals and catalyst matches.",
    )
    parser.add_argument(
        "--signals",
        default=str(DEFAULT_SIGNAL_SUMMARY_PATH),
        help="Input signal summary CSV path.",
    )
    parser.add_argument(
        "--catalysts",
        default=str(DEFAULT_CATALYST_MATCHES_PATH),
        help="Input catalyst matches CSV path.",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_PATH),
        help="Output team intelligence CSV path.",
    )
    parser.add_argument(
        "--provider",
        default="",
        help="Optional provider filter, for example: polymarket.",
    )
    return parser.parse_args()


def read_optional_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()


def clean_text(value: object) -> str:
    if pd.isna(value):
        return ""

    return str(value).strip()


def ensure_columns(dataframe: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    working = dataframe.copy()

    for column in columns:
        if column not in working.columns:
            working[column] = ""

    return working


def normalize_provider_filter(dataframe: pd.DataFrame, provider: str) -> pd.DataFrame:
    if dataframe.empty or not provider:
        return dataframe

    if "provider" not in dataframe.columns:
        return dataframe

    return dataframe[
        dataframe["provider"].astype(str).str.lower() == provider.lower()
    ].copy()


def classify_signal_direction(signal_label: str) -> str:
    label = signal_label.lower()

    if "positive" in label:
        return "positive"

    if "negative" in label:
        return "negative"

    return "flat"


def signal_rank(signal_label: str) -> int:
    label = signal_label.lower()

    if "strong_positive" in label or "strong_negative" in label:
        return 3

    if "moderate_positive" in label or "moderate_negative" in label:
        return 2

    if "flat" in label:
        return 1

    return 0


def choose_strongest_signal(labels: list[str]) -> str:
    cleaned = [clean_text(label) for label in labels if clean_text(label)]

    if not cleaned:
        return ""

    return sorted(cleaned, key=signal_rank, reverse=True)[0]


def parse_dates(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, errors="coerce", utc=True)


def format_latest_date(series: pd.Series) -> str:
    if series.empty:
        return ""

    parsed = parse_dates(series)
    parsed = parsed.dropna()

    if parsed.empty:
        return ""

    return parsed.max().strftime("%Y-%m-%d")


def build_summary_label(
    total_signals: int,
    positive_signals: int,
    negative_signals: int,
    matched_catalysts: int,
    unmatched_signals: int,
    strongest_signal: str,
) -> str:
    if total_signals == 0:
        return "no_signals"

    strongest = strongest_signal.lower()

    if matched_catalysts > 0 and "strong" in strongest:
        return "strong_signal_with_catalyst"

    if matched_catalysts > 0:
        return "signal_with_catalyst"

    if unmatched_signals > 0 and "strong" in strongest:
        return "strong_signal_needs_manual_review"

    if positive_signals > negative_signals:
        return "net_positive_attention"

    if negative_signals > positive_signals:
        return "net_negative_attention"

    return "monitor"


def build_review_priority(
    summary_label: str,
    high_confidence_catalysts: int,
    medium_confidence_catalysts: int,
    unmatched_signals: int,
) -> str:
    if summary_label == "strong_signal_needs_manual_review":
        return "high"

    if high_confidence_catalysts > 0:
        return "high"

    if medium_confidence_catalysts > 0:
        return "medium"

    if unmatched_signals > 0:
        return "medium"

    if summary_label in {"signal_with_catalyst", "net_positive_attention", "net_negative_attention"}:
        return "medium"

    return "low"


def generate_team_intelligence(
    signals: pd.DataFrame,
    catalysts: pd.DataFrame,
    provider_filter: str,
) -> pd.DataFrame:
    signal_columns = [
        "generated_at",
        "provider",
        "team",
        "signal_label",
    ]

    catalyst_columns = [
        "generated_at",
        "provider",
        "team",
        "match_type",
        "catalyst_date",
        "catalyst_confidence",
    ]

    signals = ensure_columns(signals, signal_columns)
    catalysts = ensure_columns(catalysts, catalyst_columns)

    signals = normalize_provider_filter(signals, provider_filter)
    catalysts = normalize_provider_filter(catalysts, provider_filter)

    if signals.empty and catalysts.empty:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)

    teams = sorted(
        set(signals["team"].astype(str).str.strip())
        | set(catalysts["team"].astype(str).str.strip())
    )

    teams = [team for team in teams if team]

    output_rows = []

    for team in teams:
        team_signals = signals[
            signals["team"].astype(str).str.strip() == team
        ].copy()

        team_catalysts = catalysts[
            catalysts["team"].astype(str).str.strip() == team
        ].copy()

        provider_values = []

        if not team_signals.empty:
            provider_values.extend(team_signals["provider"].astype(str).str.strip().tolist())

        if not team_catalysts.empty:
            provider_values.extend(team_catalysts["provider"].astype(str).str.strip().tolist())

        provider_values = [value for value in provider_values if value]
        provider = provider_filter or (provider_values[0] if provider_values else "")

        signal_labels = team_signals["signal_label"].astype(str).str.strip().tolist()

        total_signals = len(team_signals)
        positive_signals = sum(
            classify_signal_direction(label) == "positive"
            for label in signal_labels
        )
        negative_signals = sum(
            classify_signal_direction(label) == "negative"
            for label in signal_labels
        )
        flat_signals = sum(
            classify_signal_direction(label) == "flat"
            for label in signal_labels
        )

        matched_rows = team_catalysts[
            team_catalysts["match_type"].astype(str).str.strip() != "unmatched"
        ].copy()

        unmatched_rows = team_catalysts[
            team_catalysts["match_type"].astype(str).str.strip() == "unmatched"
        ].copy()

        matched_catalysts = len(matched_rows)
        unmatched_signals = len(unmatched_rows)

        confidence_values = matched_rows["catalyst_confidence"].astype(str).str.lower().str.strip()

        high_confidence_catalysts = int((confidence_values == "high").sum())
        medium_confidence_catalysts = int((confidence_values == "medium").sum())
        low_confidence_catalysts = int((confidence_values == "low").sum())

        strongest_signal = choose_strongest_signal(signal_labels)

        latest_signal_date = format_latest_date(team_signals["generated_at"])
        latest_catalyst_date = format_latest_date(matched_rows["catalyst_date"])

        summary_label = build_summary_label(
            total_signals=total_signals,
            positive_signals=positive_signals,
            negative_signals=negative_signals,
            matched_catalysts=matched_catalysts,
            unmatched_signals=unmatched_signals,
            strongest_signal=strongest_signal,
        )

        review_priority = build_review_priority(
            summary_label=summary_label,
            high_confidence_catalysts=high_confidence_catalysts,
            medium_confidence_catalysts=medium_confidence_catalysts,
            unmatched_signals=unmatched_signals,
        )

        output_rows.append(
            {
                "team": team,
                "provider": provider,
                "total_signals": total_signals,
                "positive_signals": positive_signals,
                "negative_signals": negative_signals,
                "flat_signals": flat_signals,
                "matched_catalysts": matched_catalysts,
                "unmatched_signals": unmatched_signals,
                "high_confidence_catalysts": high_confidence_catalysts,
                "medium_confidence_catalysts": medium_confidence_catalysts,
                "low_confidence_catalysts": low_confidence_catalysts,
                "strongest_signal": strongest_signal,
                "latest_signal_date": latest_signal_date,
                "latest_catalyst_date": latest_catalyst_date,
                "summary_label": summary_label,
                "review_priority": review_priority,
            }
        )

    if not output_rows:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)

    result = pd.DataFrame(output_rows)[OUTPUT_COLUMNS]

    priority_rank = {
        "high": 3,
        "medium": 2,
        "low": 1,
    }

    result["_priority_rank"] = result["review_priority"].map(priority_rank).fillna(0)
    result = result.sort_values(
        by=[
            "_priority_rank",
            "matched_catalysts",
            "total_signals",
            "team",
        ],
        ascending=[False, False, False, True],
    ).drop(columns=["_priority_rank"])

    return result


def main() -> None:
    args = parse_args()

    signals_path = Path(args.signals)
    catalysts_path = Path(args.catalysts)
    output_path = Path(args.output)
    provider_filter = str(args.provider).strip()

    signals = read_optional_csv(signals_path)
    catalysts = read_optional_csv(catalysts_path)

    result = generate_team_intelligence(
        signals=signals,
        catalysts=catalysts,
        provider_filter=provider_filter,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_path, index=False)

    print("Team intelligence summary")
    print(f"Signals input:        {signals_path}")
    print(f"Catalysts input:      {catalysts_path}")
    print(f"Output:               {output_path}")
    print(f"Signal rows:          {len(signals)}")
    print(f"Catalyst rows:        {len(catalysts)}")
    print(f"Team rows generated:  {len(result)}")
    print(f"Provider filter:      {provider_filter or 'none'}")


if __name__ == "__main__":
    main()
