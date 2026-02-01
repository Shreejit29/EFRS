def process_processed_data(df):
    rename_map = {
        "cycle number": "cycle_index",
        "charge capacity": "Q_charge",
        "discharge capacity": "Q_discharge",
        "charge energy": "E_charge",
        "discharge energy": "E_discharge"
    }

    df = df.rename(columns=rename_map)

    required = ["cycle_index", "Q_charge", "Q_discharge", "E_charge", "E_discharge"]

    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    return df[required]
