# phase1/io_loader.py

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Union, IO

from .config import (
    TIME_COL,
    CURRENT_COL,
    VOLTAGE_COL,
)

REQUIRED_COLUMNS = [TIME_COL, CURRENT_COL, VOLTAGE_COL]


class RawDataLoader:
    """
    Handles loading and basic normalization of raw battery data.
    Supports file paths and file-like objects (e.g. Streamlit uploads).
    """

    def __init__(self, source: Union[str, Path, IO]):
        self.source = source

    def load(self) -> pd.DataFrame:
        """
        Load CSV and perform basic sanity checks.
        """
        df = self._read_csv()
        self._validate_columns(df)
        df = self._normalize(df)
        return df

    def _read_csv(self) -> pd.DataFrame:
        """
        Read CSV from path or file-like object.
        """
        # Case 1: filepath (str or Path)
        if isinstance(self.source, (str, Path)):
            path = Path(self.source)
            if not path.exists():
                raise FileNotFoundError(f"File not found: {path}")
            return pd.read_csv(path)

        # Case 2: file-like object (Streamlit UploadedFile)
        return pd.read_csv(self.source)

    @staticmethod
    def _validate_columns(df: pd.DataFrame):
        missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

    @staticmethod
    def _normalize(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        # Sort by time
        df = df.sort_values(TIME_COL).reset_index(drop=True)

        # Enforce numeric types
        for col in REQUIRED_COLUMNS:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # Drop invalid rows
        df = df.dropna(subset=REQUIRED_COLUMNS)

        return df
