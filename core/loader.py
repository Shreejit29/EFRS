import pandas as pd

def load_file(uploaded_file):
    name = uploaded_file.name.lower()

    if name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif name.endswith(".xls") or name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
    else:
        raise ValueError("Only CSV or Excel files supported")

    df.columns = df.columns.str.strip().str.lower()
    return df
