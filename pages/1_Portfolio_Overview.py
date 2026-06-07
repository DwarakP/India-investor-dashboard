import streamlit as st
import pandas as pd

st.title("📊 Portfolio Overview")

df = pd.read_csv("data/Investments.csv")

st.dataframe(df, use_container_width=True)

st.write(f"Total Holdings: {len(df)}")
