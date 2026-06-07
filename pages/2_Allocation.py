import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📈 Allocation")

df = pd.read_csv("data/investments.csv")

top = df.sort_values(
    "Current Value",
    ascending=False
)

fig = px.pie(
    top.head(10),
    values="Current Value",
    names="Name",
    title="Top 10 Holdings"
)

st.plotly_chart(fig, use_container_width=True)
