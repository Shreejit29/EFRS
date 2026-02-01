# phase1/config.py

import numpy as np

# ---------- Mathematical Constants ----------
CEF_EXP_FACTOR = 10.0     # locked
CEF_SCALE = 2.0           # locked

# ---------- Numerical Safety ----------
EPS = 1e-9                # avoid divide-by-zero

# ---------- Column Names (standardized) ----------
TIME_COL = "time"
CURRENT_COL = "current"
VOLTAGE_COL = "voltage"

# ---------- Derived Output Columns ----------
OUTPUT_COLUMNS = [
    "Cycle_Number",
    "Charge_Capacity",
    "Discharge_Capacity",
    "Charge_Energy",
    "Discharge_Energy",
    "CE",
    "EE",
    "CEF",
]
