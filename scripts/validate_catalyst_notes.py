from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from wcmi.catalyst_notes import (
    CATALYST_NOTE_COLUMNS,
    DEFAULT_CATALYST_NOTES_PATH,
    load_catalyst_notes,
)


ALLOWED_EVENT_TYPES = {
    "",
    "match_result",
    "injury",
    "squad_announcement",
    "manager_change",
    "tactical_change",
    "media_narrative",
    "liquidity_spike",
    "bracket_implication",
    "market_structure",
    "other",
}

ALLOWED_CONFIDENCE_VALUES = {
    "",
    "low",
    "medium",
    "high",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate manual catalyst notes CSV.",
    )
    parser.add_argument(
        "--path",
        default=str(DEFAULT_CATALYST_NOTES_PATH),
        help="Path to catalyst notes CSV file.",
    )
    return parser.parse_args()


def validate_required_columns(raw_dataframe: pd.DataFrame) -> list[str]:
    errors = []

    missing_columns = [
        column
        for column in CATALYST_NOTE_COLUMNS
        if column not in raw_dataframe.columns
    ]

    if missing_columns:
        errors.append(
            "Missing required columns: " + ", ".join(missing_columns)
        )

    return errors


def validate_allowed_values(notes: pd.DataFrame) -> list[str]:
    errors = []

    invalid_event_types = sorted(
        set(notes["event_type"].astype(str).str.strip()) - ALLOWED_EVENT_TYPES
    )

    if invalid_event_types:
        errors.append(
            "Invalid event_type values: " + ", ".join(invalid_event_types)
        )

    invalid_confidence_values = sorted(
        set(notes["confidence"].astype(str).str.strip()) - ALLOWED_CONFIDENCE_VALUES
    )

    if invalid_confidence_values:
        errors.append(
            "Invalid confidence values: " + ", ".join(invalid_confidence_values)
        )

    return errors


def validate_dates(notes: pd.DataFrame) -> list[str]:
    errors = []

    non_empty_dates = notes[
        notes["date"].astype(str).str.strip() != ""
    ].copy()

    if non_empty_dates.empty:
        return errors

    parsed_dates = pd.to_datetime(
        non_empty_dates["date"],
        errors="coerce",
        utc=False,
    )

    invalid_rows = parsed_dates[parsed_dates.isna()]

    if not invalid_rows.empty:
        row_numbers = [
            str(index + 2)
            for index in invalid_rows.index
        ]
        errors.append(
            "Invalid date values on CSV row(s): " + ", ".join(row_numbers)
        )

    return errors


def validate_required_note_fields(notes: pd.DataFrame) -> list[str]:
    errors = []

    if notes.empty:
        return errors

    required_when_row_exists = [
        "date",
        "provider",
        "team",
        "event_type",
        "event_title",
        "note",
        "confidence",
        "created_by",
    ]

    for column in required_when_row_exists:
        empty_rows = notes[
            notes[column].astype(str).str.strip() == ""
        ]

        if not empty_rows.empty:
            row_numbers = [
                str(index + 2)
                for index in empty_rows.index
            ]
            errors.append(
                f"Missing {column} on CSV row(s): " + ", ".join(row_numbers)
            )

    return errors


def validate_catalyst_notes(path: Path) -> tuple[bool, list[str], pd.DataFrame]:
    if not path.exists():
        return False, [f"Catalyst notes file not found: {path}"], pd.DataFrame()

    raw_dataframe = pd.read_csv(path)

    errors = []
    errors.extend(validate_required_columns(raw_dataframe))

    if errors:
        return False, errors, raw_dataframe

    notes = load_catalyst_notes(path)

    errors.extend(validate_allowed_values(notes))
    errors.extend(validate_dates(notes))
    errors.extend(validate_required_note_fields(notes))

    return len(errors) == 0, errors, notes


def main() -> None:
    args = parse_args()
    path = Path(args.path)

    is_valid, errors, notes = validate_catalyst_notes(path)

    print("Catalyst notes validation")
    print(f"Path: {path}")
    print(f"Rows: {len(notes)}")
    print("")

    if is_valid:
        print("Result: PASS")

        if notes.empty:
            print("Status: empty template")
        else:
            print("Status: catalyst notes available")

        return

    print("Result: FAIL")
    print("")

    for error in errors:
        print(f"- {error}")

    raise SystemExit(1)


if __name__ == "__main__":
    main()
