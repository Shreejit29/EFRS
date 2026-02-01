# phase1/metrics.py

import pandas as pd
import numpy as np

from .config import (
    TIME_COL,
    CURRENT_COL,
    VOLTAGE_COL,
    EPS,
    CEF_EXP_FACTOR,
    CEF_SCALE,
)


class CycleMetrics:
    """
    Computes per-cycle capacity, energy, CE, EE, and CEF.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def compute(self) -> pd.DataFrame:
        """
        Returns a per-cycle summary DataFrame.
        """
        self._compute_time_delta()
        cycle_groups = self.df.groupby("Cycle_Number")

        records = []

        for cycle, g in cycle_groups:
            record = self._compute_single_cycle(cycle, g)
            records.append(record)

        return pd.DataFrame(records)

    def _compute_time_delta(self):
        """
        Compute dt in seconds between samples.
        """
        self.df["dt"] = self.df[TIME_COL].diff()
        self.df["dt"] = self.df["dt"].fillna(0)

    def _compute_single_cycle(self, cycle_number: int, g: pd.DataFrame) -> dict:
        """
        Compute metrics for a single cycle.
        """
        # Separate charge and discharge
        chg = g[g["step_type"] == "charge"]
        dis = g[g["step_type"] == "discharge"]

        # Capacity (Ah)
        Q_chg = np.sum(chg[CURRENT_COL] * chg["dt"]) / 3600.0
        Q_dis = -np.sum(dis[CURRENT_COL] * dis["dt"]) / 3600.0

        # Energy (Wh)
        E_chg = np.sum(
            chg[VOLTAGE_COL] * chg[CURRENT_COL] * chg["dt"]
        ) / 3600.0

        E_dis = -np.sum(
            dis[VOLTAGE_COL] * dis[CURRENT_COL] * dis["dt"]
        ) / 3600.0

        # Efficiencies
        CE = Q_dis / (Q_chg + EPS)
        EE = E_dis / (E_chg + EPS)

        # CEF (LOCKED FORMULA)
        CEF = CEF_SCALE / (
            (1 / np.exp(-CEF_EXP_FACTOR * (1 - CE))) +
            (1 / np.exp(-CEF_EXP_FACTOR * (1 - EE)))
        )

        return {
            "Cycle_Number": cycle_number,
            "Charge_Capacity": Q_chg,
            "Discharge_Capacity": Q_dis,
            "Charge_Energy": E_chg,
            "Discharge_Energy": E_dis,
            "CE": CE,
            "EE": EE,
            "CEF": CEF,
        }
