import pandas as pd
from pathlib import Path

def load_file(filepath: str) -> pd.DataFrame:
    path = Path(filepath)

    if path.suffix.lower() == ".csv":
        df = pd.read_csv(path)
    elif path.suffix.lower() in [".xls", ".xlsx"]:
        df = pd.read_excel(path)
    else:
        raise ValueError("Unsupported file format")

    df.columns = df.columns.str.strip().str.lower()
    return df
