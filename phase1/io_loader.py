# phase1/io_loader.py

import pandas as pd
from pathlib import Path
from typing import Union, IO
from io import BytesIO

from .config import (
    TIME_COL,
    CURRENT_COL,
    VOLTAGE_COL,
)

REQUIRED_COLUMNS = [TIME_COL, CURRENT_COL, VOLTAGE_COL]


class RawDataLoader:
    """
    Handles loading and basic normalization of raw battery data.
    Supports:
    - file paths (str / Path)
    - Streamlit UploadedFile (file-like)
    """

    def __init__(self, source: Union[str, Path, IO]):
        self.source = source

    def load(self) -> pd.DataFrame:
        df = self._read_csv()
        self._validate_columns(df)
        df = self._normalize(df)
        return df

    def _read_csv(self) -> pd.DataFrame:
        """
        Read CSV from path or file-like object safely.
        """

        # Case 1: File path
        if isinstance(self.source, (str, Path)):
            path = Path(self.source)
            if not path.exists():
                raise FileNotFoundError(f"File not found: {path}")
            return pd.read_csv(path)

        # Case 2: Streamlit UploadedFile or file-like object
        try:
            bytes_data = self.source.read()
            return pd.read_csv(BytesIO(bytes_data))
        except Exception as e:
            raise TypeError(
                "Unsupported file input type. "
                "Expected file path or file-like object."
            ) from e

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
