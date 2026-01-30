import numpy as np

def assign_cycles(df, current_col="current"):
    current = df[current_col].values
    sign = np.sign(current)

    cycle_index = []
    cycle = 0
    last_sign = sign[0]

    for s in sign:
        if s < 0 and last_sign > 0:
            cycle += 1
        cycle_index.append(cycle)
        last_sign = s

    df["cycle_index"] = cycle_index
    return df
