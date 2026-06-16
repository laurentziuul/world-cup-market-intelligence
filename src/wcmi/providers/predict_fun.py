from __future__ import annotations

import pandas as pd

from wcmi.providers.base import MarketProvider


class PredictFunProvider(MarketProvider):
    name = "predict_fun"

    def load(self) -> pd.DataFrame:
        raise NotImplementedError(
            "PredictFunProvider is planned but not implemented yet. "
            "Use manual_csv for the stable offline pipeline."
        )