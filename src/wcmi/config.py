from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    gamma_base_url: str = os.getenv("POLYMARKET_GAMMA_BASE_URL", "https://gamma-api.polymarket.com")
    event_query: str = os.getenv("WCMI_EVENT_QUERY", "world cup")
    output_dir: Path = Path(os.getenv("WCMI_OUTPUT_DIR", "briefs"))
    data_raw_dir: Path = Path("data/raw")
    data_processed_dir: Path = Path("data/processed")
    watchlist_path: Path = Path("data/watchlist.csv")


settings = Settings()
