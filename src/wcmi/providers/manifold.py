from __future__ import annotations

import pandas as pd

from wcmi.providers.base import MarketProvider


class ManifoldProvider(MarketProvider):
    name = "manifold"

    def load(self) -> pd.DataFrame:
        raise NotImplementedError(
            "ManifoldProvider is planned but not implemented yet. "
            "Use manual_csv for the stable offline pipeline."
        )