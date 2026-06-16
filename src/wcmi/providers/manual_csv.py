from __future__ import annotations

from pathlib import Path

import pandas as pd

from wcmi.providers.base import MarketProvider, normalize_provider_dataframe, project_root_from_file


class ManualCsvProvider(MarketProvider):
    name = "manual_csv"

    def __init__(self, input_path: Path | None = None) -> None:
        root = project_root_from_file(__file__)
        self.input_path = input_path or root / "data" / "manual" / "world_cup_markets.csv"

    def load(self) -> pd.DataFrame:
        if not self.input_path.exists():
            raise FileNotFoundError(
                f"Manual CSV input file not found: {self.input_path}\n"
                "Create data/manual/world_cup_markets.csv first."
            )

        df = pd.read_csv(self.input_path)

        return normalize_provider_dataframe(df, provider_name=self.name)