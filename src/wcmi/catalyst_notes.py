from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]

DEFAULT_CATALYST_NOTES_PATH = ROOT / "data" / "manual" / "catalyst_notes.csv"

CATALYST_NOTE_COLUMNS = [
    "date",
    "provider",
    "team",
    "market_id",
    "market_title",
    "event_type",
    "event_title",
    "note",
    "source_url",
    "confidence",
    "created_by",
]

TEXT_COLUMNS = [
    "provider",
    "team",
    "market_id",
    "market_title",
    "event_type",
    "event_title",
    "note",
    "source_url",
    "confidence",
    "created_by",
]


def empty_catalyst_notes() -> pd.DataFrame:
    return pd.DataFrame(columns=CATALYST_NOTE_COLUMNS)


def ensure_catalyst_note_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    working = dataframe.copy()

    for column in CATALYST_NOTE_COLUMNS:
        if column not in working.columns:
            working[column] = ""

    return working[CATALYST_NOTE_COLUMNS].copy()


def normalize_catalyst_notes(dataframe: pd.DataFrame) -> pd.DataFrame:
    working = ensure_catalyst_note_columns(dataframe)

    for column in TEXT_COLUMNS:
        working[column] = working[column].fillna("").astype(str).str.strip()

    working["date"] = working["date"].fillna("").astype(str).str.strip()

    return working


def load_catalyst_notes(path: Path | str | None = None) -> pd.DataFrame:
    notes_path = Path(path) if path else DEFAULT_CATALYST_NOTES_PATH

    if not notes_path.exists():
        raise FileNotFoundError(f"Catalyst notes file not found: {notes_path}")

    dataframe = pd.read_csv(notes_path)

    return normalize_catalyst_notes(dataframe)


def has_catalyst_notes(path: Path | str | None = None) -> bool:
    notes = load_catalyst_notes(path)
    return not notes.empty


def print_catalyst_notes_summary(path: Path | str | None = None) -> None:
    notes_path = Path(path) if path else DEFAULT_CATALYST_NOTES_PATH
    notes = load_catalyst_notes(notes_path)

    print("Catalyst notes loader")
    print(f"Path:    {notes_path}")
    print(f"Columns: {len(notes.columns)}")
    print(f"Rows:    {len(notes)}")

    if notes.empty:
        print("Status:  empty template")
    else:
        print("Status:  notes available")