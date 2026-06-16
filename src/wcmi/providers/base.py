from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd


NORMALIZED_COLUMNS = [
    "market_id",
    "market_title",
    "outcome",
    "price",
    "volume",
    "liquidity",
    "narrative",
    "catalyst",
    "source_url",
    "notes",
]

NUMERIC_COLUMNS = [
    "price",
    "volume",
    "liquidity",
]


class MarketProvider(ABC):
    """
    Base class for all market data providers.

    A provider loads raw market data from one source and returns a normalized
    pandas DataFrame with the columns required by the snapshot pipeline.
    """

    name: str

    @abstractmethod
    def load(self) -> pd.DataFrame:
        """Return normalized market data."""
        raise NotImplementedError


def validate_required_columns(df: pd.DataFrame, required_columns: list[str] | None = None) -> None:
    required = required_columns or NORMALIZED_COLUMNS
    missing = [column for column in required if column not in df.columns]

    if missing:
        raise ValueError(f"Missing required provider columns: {missing}")


def normalize_provider_dataframe(df: pd.DataFrame, provider_name: str) -> pd.DataFrame:
    """
    Normalize provider output into the canonical internal market schema.
    """

    df = df.copy()

    validate_required_columns(df)

    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

    for column in NORMALIZED_COLUMNS:
        if column not in df.columns:
            df[column] = ""

    df["provider"] = provider_name

    return df[NORMALIZED_COLUMNS + ["provider"]]


def project_root_from_file(file_path: str | Path) -> Path:
    """
    Resolve project root from a file inside src/wcmi/providers/.

    Expected file location:
    src/wcmi/providers/<provider>.py
    """

    return Path(file_path).resolve().parents[3]