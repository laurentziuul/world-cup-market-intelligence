from __future__ import annotations

import argparse
from datetime import timedelta
from pathlib import Path

import pandas as pd

from wcmi.catalyst_notes import (
    DEFAULT_CATALYST_NOTES_PATH,
    load_catalyst_notes,
)


ROOT = Path(__file__).resolve().parents[1]

DEFAULT_SIGNAL_SUMMARY_PATH = ROOT / "data" / "processed" / "signal_summary_latest.csv"
DEFAULT_OUTPUT_PATH = ROOT / "data" / "processed" / "catalyst_matches_latest.csv"


OUTPUT_COLUMNS = [
    "generated_at",
    "provider",
    "team",
    "market_id",
    "market_title",
    "outcome",
    "signal_label",
    "signal_strength",
    "probability_change_display",
    "liquidity_label",
    "signal_reason",
    "catalyst_date",
    "event_type",
    "event_title",
    "catalyst_note",
    "catalyst_source_url",
    "catalyst_confidence",
    "catalyst_created_by",
    "match_type",
    "match_reason",
    "signal_source_url",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Match catalyst notes to signal summary rows.",
    )
    parser.add_argument(
        "--input",
        default=str(DEFAULT_SIGNAL_SUMMARY_PATH),
        help="Input signal summary CSV path.",
    )
    parser.add_argument(
        "--notes-path",
        default=str(DEFAULT_CATALYST_NOTES_PATH),
        help="Catalyst notes CSV path.",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_PATH),
        help="Output catalyst matches CSV path.",
    )
    parser.add_argument(
        "--provider",
        default="",
        help="Optional provider filter, for example: polymarket.",
    )
    parser.add_argument(
        "--team",
        default="",
        help="Optional team filter.",
    )
    parser.add_argument(
        "--lookback-days",
        type=int,
        default=7,
        help="Match catalyst notes from this many days before the signal timestamp.",
    )
    parser.add_argument(
        "--include-unmatched",
        action="store_true",
        help="Include signal rows even when no catalyst note matches.",
    )
    return parser.parse_args()


def require_columns(dataframe: pd.DataFrame, columns: list[str], name: str) -> None:
    missing = [
        column
        for column in columns
        if column not in dataframe.columns
    ]

    if missing:
        raise SystemExit(
            f"Missing required columns in {name}: " + ", ".join(missing)
        )


def clean_text(value: object) -> str:
    if pd.isna(value):
        return ""

    return str(value).strip()


def normalize_key(value: object) -> str:
    return clean_text(value).lower()


def parse_datetime_series(series: pd.Series) -> pd.Series:
    return pd.to_datetime(
        series,
        errors="coerce",
        utc=True,
    )


def parse_date_series(series: pd.Series) -> pd.Series:
    parsed = pd.to_datetime(
        series,
        errors="coerce",
        utc=True,
    )

    return parsed


def filter_signal_summary(
    signals: pd.DataFrame,
    provider_filter: str,
    team_filter: str,
) -> pd.DataFrame:
    working = signals.copy()

    if provider_filter:
        working = working[
            working["provider"].astype(str).str.lower()
            == provider_filter.lower()
        ].copy()

    if team_filter:
        working = working[
            working["team"].astype(str).str.lower()
            == team_filter.lower()
        ].copy()

    return working


def note_matches_signal(
    signal: pd.Series,
    note: pd.Series,
    lookback_days: int,
) -> tuple[bool, str, str]:
    signal_provider = normalize_key(signal.get("provider", ""))
    signal_team = normalize_key(signal.get("team", ""))
    signal_market_id = normalize_key(signal.get("market_id", ""))
    signal_generated_at = signal.get("_generated_at_parsed")

    note_provider = normalize_key(note.get("provider", ""))
    note_team = normalize_key(note.get("team", ""))
    note_market_id = normalize_key(note.get("market_id", ""))
    note_date = note.get("_note_date_parsed")

    if note_provider and signal_provider and note_provider != signal_provider:
        return False, "", "provider mismatch"

    if note_market_id and signal_market_id:
        if note_market_id != signal_market_id:
            return False, "", "market_id mismatch"

        base_match_type = "market_id"
    else:
        if not note_team or not signal_team or note_team != signal_team:
            return False, "", "team mismatch"

        base_match_type = "team"

    if pd.notna(signal_generated_at) and pd.notna(note_date):
        start_date = signal_generated_at - timedelta(days=lookback_days)
        end_date = signal_generated_at + timedelta(days=1)

        if note_date < start_date or note_date > end_date:
            return False, "", "outside date window"

        return (
            True,
            f"{base_match_type}+date_window",
            f"matched by {base_match_type} within {lookback_days}-day lookback",
        )

    return (
        True,
        base_match_type,
        f"matched by {base_match_type}; date window unavailable",
    )


def build_output_row(
    signal: pd.Series,
    note: pd.Series | None,
    match_type: str,
    match_reason: str,
) -> dict[str, object]:
    return {
        "generated_at": clean_text(signal.get("generated_at", "")),
        "provider": clean_text(signal.get("provider", "")),
        "team": clean_text(signal.get("team", "")),
        "market_id": clean_text(signal.get("market_id", "")),
        "market_title": clean_text(signal.get("market_title", "")),
        "outcome": clean_text(signal.get("outcome", "")),
        "signal_label": clean_text(signal.get("signal_label", "")),
        "signal_strength": clean_text(signal.get("signal_strength", "")),
        "probability_change_display": clean_text(
            signal.get("probability_change_display", "")
        ),
        "liquidity_label": clean_text(signal.get("liquidity_label", "")),
        "signal_reason": clean_text(signal.get("signal_reason", "")),
        "catalyst_date": clean_text(note.get("date", "")) if note is not None else "",
        "event_type": clean_text(note.get("event_type", "")) if note is not None else "",
        "event_title": clean_text(note.get("event_title", "")) if note is not None else "",
        "catalyst_note": clean_text(note.get("note", "")) if note is not None else "",
        "catalyst_source_url": clean_text(note.get("source_url", "")) if note is not None else "",
        "catalyst_confidence": clean_text(note.get("confidence", "")) if note is not None else "",
        "catalyst_created_by": clean_text(note.get("created_by", "")) if note is not None else "",
        "match_type": match_type,
        "match_reason": match_reason,
        "signal_source_url": clean_text(signal.get("source_url", "")),
    }


def match_catalyst_notes(
    signals: pd.DataFrame,
    notes: pd.DataFrame,
    provider_filter: str,
    team_filter: str,
    lookback_days: int,
    include_unmatched: bool,
) -> pd.DataFrame:
    require_columns(
        signals,
        [
            "generated_at",
            "provider",
            "team",
            "market_id",
            "market_title",
            "outcome",
            "signal_label",
            "signal_strength",
            "probability_change_display",
            "liquidity_label",
            "signal_reason",
            "source_url",
        ],
        "signal summary",
    )

    signals = filter_signal_summary(
        signals=signals,
        provider_filter=provider_filter,
        team_filter=team_filter,
    )

    signals = signals.copy()
    notes = notes.copy()

    signals["_generated_at_parsed"] = parse_datetime_series(signals["generated_at"])
    notes["_note_date_parsed"] = parse_date_series(notes["date"])

    output_rows = []

    for _, signal in signals.iterrows():
        matched_any = False

        for _, note in notes.iterrows():
            is_match, match_type, match_reason = note_matches_signal(
                signal=signal,
                note=note,
                lookback_days=lookback_days,
            )

            if not is_match:
                continue

            matched_any = True
            output_rows.append(
                build_output_row(
                    signal=signal,
                    note=note,
                    match_type=match_type,
                    match_reason=match_reason,
                )
            )

        if include_unmatched and not matched_any:
            output_rows.append(
                build_output_row(
                    signal=signal,
                    note=None,
                    match_type="unmatched",
                    match_reason="no catalyst note matched",
                )
            )

    if not output_rows:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)

    return pd.DataFrame(output_rows)[OUTPUT_COLUMNS]


def main() -> None:
    args = parse_args()

    input_path = Path(args.input)
    notes_path = Path(args.notes_path)
    output_path = Path(args.output)

    if not input_path.exists():
        raise SystemExit(
            f"Input file does not exist: {input_path}\n"
            "Run scripts/run_historical_trends_workflow.py first."
        )

    signals = pd.read_csv(input_path)
    notes = load_catalyst_notes(notes_path)

    matches = match_catalyst_notes(
        signals=signals,
        notes=notes,
        provider_filter=str(args.provider).strip(),
        team_filter=str(args.team).strip(),
        lookback_days=int(args.lookback_days),
        include_unmatched=bool(args.include_unmatched),
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    matches.to_csv(output_path, index=False)

    print("Catalyst notes matching")
    print(f"Signals input:       {input_path}")
    print(f"Catalyst notes input: {notes_path}")
    print(f"Output:              {output_path}")
    print(f"Signal rows:         {len(signals)}")
    print(f"Catalyst note rows:  {len(notes)}")
    print(f"Matched rows:        {len(matches)}")
    print(f"Provider filter:     {args.provider or 'none'}")
    print(f"Team filter:         {args.team or 'none'}")
    print(f"Lookback days:       {args.lookback_days}")
    print(f"Include unmatched:   {args.include_unmatched}")


if __name__ == "__main__":
    main()
