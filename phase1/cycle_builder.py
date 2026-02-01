# phase1/cycle_builder.py

import pandas as pd
import numpy as np

from .config import CURRENT_COL


class CycleBuilder:
    """
    Detects charge/discharge segments and assigns cycle numbers.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def build_cycles(self) -> pd.DataFrame:
        """
        Adds two columns:
        - step_type: 'charge', 'discharge', or 'rest'
        - Cycle_Number: integer cycle index (starts at 1)
        """
        self._classify_step_type()
        self._assign_cycle_numbers()
        return self.df

    def _classify_step_type(self):
        """
        Classify each row based on current sign.
        """
        conditions = [
            self.df[CURRENT_COL] > 0,
            self.df[CURRENT_COL] < 0,
        ]
        choices = ["charge", "discharge"]

        self.df["step_type"] = np.select(
            conditions, choices, default="rest"
        )

    def _assign_cycle_numbers(self):
        """
        Assign cycle numbers based on discharge completion.
        """
        cycle_number = 0
        in_charge = False
        in_discharge = False

        cycle_numbers = []

        for step in self.df["step_type"]:
            if step == "charge":
                in_charge = True
                in_discharge = False

            elif step == "discharge" and in_charge:
                # discharge after charge → valid cycle
                if not in_discharge:
                    cycle_number += 1
                    in_discharge = True

            elif step == "rest":
                pass

            cycle_numbers.append(
                cycle_number if cycle_number > 0 else np.nan
            )

        self.df["Cycle_Number"] = cycle_numbers

        # Drop rows before first complete cycle
        self.df = self.df.dropna(subset=["Cycle_Number"])
        self.df["Cycle_Number"] = self.df["Cycle_Number"].astype(int)
