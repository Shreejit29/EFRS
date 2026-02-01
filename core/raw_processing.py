import numpy as np
from core.loader import find_column

def process_raw_data(df):

    current_col  = find_column(df, ["current"])
    capacity_col = find_column(df, ["capacity"])
    energy_col   = find_column(df, ["energy"])

    current = df[current_col].values

    # threshold to ignore rest noise (mA level, adjust if needed)
    eps = 1e-6

    def current_state(i):
        if i > eps:
            return "charge"
        elif i < -eps:
            return "discharge"
        else:
            return "rest"

    states = [current_state(i) for i in current]

    cycle = 0
    cycles = []
    prev_state = states[0]

    for state in states:
        # NEW cycle starts when charge begins AFTER discharge
        if prev_state == "discharge" and state == "charge":
            cycle += 1

        cycles.append(cycle)
        prev_state = state

    df["cycle_index"] = cycles

    grouped = df.groupby("cycle_index")

    out = grouped.agg(
        Q_charge=(capacity_col, lambda x: x.max() - x.min()),
        E_charge=(energy_col,   lambda x: x.max() - x.min()),
    ).reset_index()

    # Phase I assumption (locked earlier)
    out["Q_discharge"] = out["Q_charge"]
    out["E_discharge"] = out["E_charge"]

    return out
