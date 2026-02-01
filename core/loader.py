import pandas as pd
import re

def load_file(uploaded_file):
    name = uploaded_file.name.lower()

    if name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif name.endswith(".xls") or name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
    else:
        raise ValueError("Only CSV or Excel files supported")

    # normalize column names (lowercase only, keep original text)
    df.columns = df.columns.str.strip().str.lower()
    return df


def normalize(text):
    return re.sub(r"[^a-z0-9]", "", text.lower())


def find_column(df, candidates):
    norm_cols = {normalize(col): col for col in df.columns}

    for key in candidates:
        key_norm = normalize(key)
        for norm_col, original_col in norm_cols.items():
            if key_norm in norm_col:
                return original_col

    raise ValueError(f"Required column not found. Tried: {candidates}")
