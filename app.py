import streamlit as st

from core.loader import load_file
from core.detector import detect_data_type
from core.raw_processing import process_raw_data
from core.processed import process_processed_data
from core.efficiency import compute_efficiencies

st.set_page_config(page_title="EFRS Phase I", layout="wide")

st.title("EFRS – Phase I: CE / EE / CEF")

uploaded_file = st.file_uploader(
    "Upload battery data file (CSV / Excel)",
    type=["csv", "xls", "xlsx"]
)

if uploaded_file:
    try:
        df = load_file(uploaded_file)
        data_type = detect_data_type(df)

        st.info(f"Detected data type: **{data_type}**")

        if data_type == "RAW":
            cycle_df = process_raw_data(df)
        else:
            cycle_df = process_processed_data(df)

        cycle_df = compute_efficiencies(cycle_df)

        st.subheader("Per-cycle CE / EE / CEF")
        st.dataframe(cycle_df)

        st.subheader("CEF vs Cycle")
        st.line_chart(cycle_df.set_index("cycle_index")["CEF"])

    except Exception as e:
        st.error(str(e))
