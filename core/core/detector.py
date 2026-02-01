def detect_data_type(df):
    cycle_cols = ["cycle", "cycle_index", "cycle number"]

    has_cycle = any(col in df.columns for col in cycle_cols)

    if not has_cycle:
        return "RAW"

    cycle_col = next(col for col in cycle_cols if col in df.columns)

    # if more than one row per cycle → RAW
    if df[cycle_col].value_counts().max() > 1:
        return "RAW"

    return "PROCESSED"
