# phase1/pipeline.py

import pandas as pd

from .io_loader import RawDataLoader
from .cycle_builder import CycleBuilder
from .metrics import CycleMetrics
from .validator import CycleValidator


class PhaseIPipeline:
    """
    End-to-end Phase I pipeline:
    Raw data → per-cycle metrics with CEF
    """

    def __init__(self, filepath: str):
        self.filepath = filepath

    def run(self) -> pd.DataFrame:
        # Step 1: Load raw data
        df_raw = RawDataLoader(self.filepath).load()

        # Step 2: Build cycles
        df_cycles = CycleBuilder(df_raw).build_cycles()

        # Step 3: Compute per-cycle metrics
        df_metrics = CycleMetrics(df_cycles).compute()

        # Step 4: Validate results
        df_valid = CycleValidator(df_metrics).validate()

        return df_valid
