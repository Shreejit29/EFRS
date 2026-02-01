import numpy as np

def compute_efficiencies(df, k=10):
    df["CE"] = df["Q_discharge"] / df["Q_charge"]
    df["EE"] = df["E_discharge"] / df["E_charge"]

    CE = df["CE"].clip(0.90, 1.05)
    EE = df["EE"].clip(0.85, 1.00)

    df["CEF"] = 2.0 / (
        np.exp(-k * (1 - CE)) +
        np.exp(-k * (1 - EE))
    )

    return df
