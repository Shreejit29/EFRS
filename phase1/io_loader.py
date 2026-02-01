# phase1/io_loader.py

import pandas as pd
from pathlib import Path
from typing import Union, IO
from io import BytesIO

from .config import TIME_COL, CURRENT_COL, VOLTAGE_COL

# -------- Column Mapping (EXPLICIT) --------
COLUMN_MAP = {
    "time": TIME_COL,
    "voltage (mv)": VOLTAGE_COL,
    "current (ma)": CURRENT_COL,
}

REQUIRED_COLUMNS = [TIME_COL, CURRENT_COL, VOLTAGE_COL]


class RawDataLoader:
    """
    Handles loading and normalization of raw battery data.
    Supports real cycler datasets with unit conversion.
    """

    def __init__(self, source: Union[str, Path, IO]):
        self.source = source

    def load(self) -> pd.DataFrame:
        df = self._read_csv()
        df = self._normalize_columns(df)
        df = self._map_columns(df)
        self._validate_columns(df)
        df = self._normalize_rows(df)
        return df

    def _read_csv(self) -> pd.DataFrame:
        if isinstance(self.source, (str, Path)):
            path = Path(self.source)
            if not path.exists():
                raise FileNotFoundError(f"File not found: {path}")
            return pd.read_csv(path)

        bytes_data = self.source.read()
        return pd.read_csv(BytesIO(bytes_data))

    @staticmethod
    def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
            .str.lower()
        )
        return df

    @staticmethod
    def _map_columns(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        for src, dst in COLUMN_MAP.items():
            if src in df.columns:
                df.rename(columns={src: dst}, inplace=True)

        return df

    @staticmethod
    def _validate_columns(df: pd.DataFrame):
        missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
        if missing:
            raise ValueError(
                f"Missing required columns: {missing}\n"
                f"Found columns: {list(df.columns)}"
            )

    @staticmethod
    def _normalize_rows(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        # Enforce numeric
        df[TIME_COL] = pd.to_numeric(df[TIME_COL], errors="coerce")
        df[CURRENT_COL] = pd.to_numeric(df[CURRENT_COL], errors="coerce")
        df[VOLTAGE_COL] = pd.to_numeric(df[VOLTAGE_COL], errors="coerce")

        # Unit conversion
        # mA → A
        df[CURRENT_COL] = df[CURRENT_COL] / 1000.0
        # mV → V
        df[VOLTAGE_COL] = df[VOLTAGE_COL] / 1000.0

        # Sort by time
        df = df.sort_values(TIME_COL).reset_index(drop=True)

        # Drop invalid rows
        df = df.dropna(subset=REQUIRED_COLUMNS)

        return df
