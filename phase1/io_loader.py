# phase1/io_loader.py

import pandas as pd
import numpy as np
from pathlib import Path

from .config import (
    TIME_COL,
    CURRENT_COL,
    VOLTAGE_COL,
)

REQUIRED_COLUMNS = [TIME_COL, CURRENT_COL, VOLTAGE_COL]


class RawDataLoader:
    """
    Handles loading and basic normalization of raw battery data.
    """

    def __init__(self, filepath: str | Path):
        self.filepath = Path(filepath)

    def load(self) -> pd.DataFrame:
        """
        Load CSV and perform basic sanity checks.
        """
        if not self.filepath.exists():
            raise FileNotFoundError(f"File not found: {self.filepath}")

        df = pd.read_csv(self.filepath)

        self._validate_columns(df)
        df = self._normalize(df)

        return df

    @staticmethod
    def _validate_columns(df: pd.DataFrame):
        """
        Ensure required columns are present.
        """
        missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

    @staticmethod
    def _normalize(df: pd.DataFrame) -> pd.DataFrame:
        """
        Basic cleaning and normalization:
        - Sort by time
        - Force numeric types
        - Drop invalid rows
        """
        df = df.copy()

        # Sort chronologically
        df = df.sort_values(TIME_COL).reset_index(drop=True)

        # Enforce numeric types
        for col in REQUIRED_COLUMNS:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # Drop rows with NaNs in critical columns
        df = df.dropna(subset=REQUIRED_COLUMNS)

        return df
