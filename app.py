"""Sarin Finances — app shell.

Skeleton only: confirms the Streamlit → Cloudflare D1 connection works.
Pages come next.
"""

import streamlit as st

from db import run_sql

st.set_page_config(page_title="Sarin Finances", page_icon="💵", layout="wide")

st.title("Sarin Finances")

try:
    rows = run_sql("SELECT 1 AS ok")
    if rows and rows[0].get("ok") == 1:
        st.success("Connected To D1")
    else:
        st.error("D1 replied, but not with the expected result.")
except Exception as exc:  # noqa: BLE001 — show any failure plainly on screen
    st.error(f"Not Connected To D1: {exc}")
