import numpy as np
import pandas as pd

def process_raw_data(df):
    # Expect columns: current, capacity, energy
    current = df["current"].values
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
        Q_charge=("capacity", lambda x: x.max() - x.min()),
        E_charge=("energy", lambda x: x.max() - x.min()),
        T_mean=("temperature", "mean") if "temperature" in df.columns else ("cycle_index", "size"),
        T_max=("temperature", "max") if "temperature" in df.columns else ("cycle_index", "size"),
    ).reset_index()

    # Placeholder: symmetric assumption (will refine later)
    out["Q_discharge"] = out["Q_charge"]
    out["E_discharge"] = out["E_charge"]

    return out
