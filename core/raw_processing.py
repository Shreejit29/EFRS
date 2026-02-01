import numpy as np
from core.loader import find_column

def process_raw_data(df):

    capacity_col = find_column(df, ["capacity"])
    energy_col   = find_column(df, ["energy"])

    capacity = df[capacity_col].values

    cycles = []
    cycle = 0

    for i in range(len(capacity)):
        if i > 0:
            # Detect capacity reset (new cycle)
            if capacity[i] < 0.1 * capacity[i-1]:
                cycle += 1
        cycles.append(cycle)

    df["cycle_index"] = cycles

    grouped = df.groupby("cycle_index")

    out = grouped.agg(
        Q_charge=(capacity_col, lambda x: x.max() - x.min()),
        E_charge=(energy_col,   lambda x: x.max() - x.min()),
    ).reset_index()

    # Phase I assumption (locked)
    out["Q_discharge"] = out["Q_charge"]
    out["E_discharge"] = out["E_charge"]

    return out
