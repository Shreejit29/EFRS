def aggregate_cycles(df):
    grouped = df.groupby("cycle_index")

    agg = grouped.agg(
        Q_charge=("capacity", lambda x: x.max() - x.min()),
        E_charge=("energy",   lambda x: x.max() - x.min()),
        T_mean=("temperature", "mean"),
        T_max=("temperature", "max"),
    ).reset_index()

    return agg
