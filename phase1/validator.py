# phase1/validator.py

import pandas as pd
import numpy as np


class CycleValidator:
    """
    Performs sanity checks on per-cycle metrics.
    """

    def __init__(self, df_cycles: pd.DataFrame):
        self.df = df_cycles.copy()

    def validate(self) -> pd.DataFrame:
        """
        Apply validation rules and return cleaned DataFrame.
        """
        self._check_efficiencies()
        return self.df

    def _check_efficiencies(self):
        """
        Remove physically invalid cycles.
        """
        conditions = (
            (self.df["CE"] > 0) &
            (self.df["CE"] <= 1.05) &
            (self.df["EE"] > 0) &
            (self.df["EE"] <= 1.05)
        )

        invalid_count = (~conditions).sum()

        if invalid_count > 0:
            # Explicit, visible behavior
            self.df = self.df[conditions].reset_index(drop=True)
