# app.py

import streamlit as st
import pandas as pd

from phase1.pipeline import PhaseIPipeline

st.set_page_config(page_title="EFRS – Phase I Test", layout="wide")

st.title("🔋 EFRS – Phase I")
st.caption("Upload raw battery data → per-cycle CE, EE, CEF")

# ---------------- File Upload ----------------
st.subheader("Upload Raw Battery Dataset")

uploaded_file = st.file_uploader(
    "Choose a CSV file (time in seconds)",
    type=["csv"]
)

if uploaded_file is None:
    st.info("Please upload a raw CSV file to proceed.")
    st.stop()

# ---------------- Run Phase I ----------------
st.subheader("Phase I Output")

try:
    pipeline = PhaseIPipeline(uploaded_file)
    df_results = pipeline.run()

    st.success("Phase I executed successfully ✔")

    st.dataframe(df_results, use_container_width=True)

except Exception as e:
    st.error("Phase I failed ❌")
    st.exception(e)
