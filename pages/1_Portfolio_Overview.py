import streamlit as st
import pandas as pd

st.title("📊 Portfolio Overview")

df = pd.read_csv(
    "data/investments.csv",
    encoding="utf-8",
    on_bad_lines="skip"
)

st.dataframe(df, use_container_width=True)

st.write(f"Total Holdings: {len(df)}")
