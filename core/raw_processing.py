import numpy as np
from core.loader import find_column

def process_raw_data(df):

    current_col  = find_column(df, ["current"])
    capacity_col = find_column(df, ["capacity"])
    energy_col   = find_column(df, ["energy"])

    current = df[current_col].values
    sign = np.sign(current)

    cycle = 0
    cycles = []

    for i in range(len(sign)):
        if i > 0 and sign[i] < 0 and sign[i-1] > 0:
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
