# app.py

import streamlit as st
import os

from phase1.pipeline import PhaseIPipeline

st.set_page_config(page_title="EFRS – Phase I Test", layout="wide")

st.title("🔋 EFRS – Phase I (Real Data)")
st.caption("Raw battery data → per-cycle CE, EE, CEF")

DATA_DIR = "data/raw"

st.subheader("Select Raw Dataset")

available_files = sorted(
    [f for f in os.listdir(DATA_DIR) if f.endswith(".csv")]
)

data_source = st.radio(
    "Data source",
    ["GitHub dataset", "Upload file"],
    horizontal=True
)

if data_source == "GitHub dataset":
    filename = st.selectbox("Choose a raw dataset", available_files)
    filepath = os.path.join(DATA_DIR, filename)
else:
    uploaded = st.file_uploader("Upload raw CSV", type=["csv"])
    if uploaded is None:
        st.stop()
    filepath = uploaded

st.divider()

# Run Phase I
st.subheader("Phase I Output")

try:
    pipeline = PhaseIPipeline(filepath)
    df_results = pipeline.run()

    st.success("Phase I executed successfully ✔")
    st.dataframe(df_results, use_container_width=True)

except Exception as e:
    st.error("Phase I failed ❌")
    st.exception(e)
