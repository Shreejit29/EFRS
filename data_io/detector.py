def detect_data_type(df):
    cycle_cols = ["cycle", "cycle_index", "cycle number"]

    has_cycle_col = any(col in df.columns for col in cycle_cols)

    if not has_cycle_col:
        return "RAW"

    # check if more than one row per cycle
    cycle_col = next(col for col in cycle_cols if col in df.columns)
    counts = df[cycle_col].value_counts()

    if counts.max() > 1:
        return "RAW"

    return "PROCESSED"
