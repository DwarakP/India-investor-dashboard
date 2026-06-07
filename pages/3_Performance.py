import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📈 Performance Analysis")

# Load portfolio
df = pd.read_csv("Investments.csv")

# Convert columns to numeric
numeric_cols = [
    "Profit/Loss",
    "Profit/Loss %",
    "Current Value",
    "Invested Value",
    "Todays Profit/Loss"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# KPIs
total_profit = df["Profit/Loss"].sum()

winners = len(df[df["Profit/Loss"] > 0])
losers = len(df[df["Profit/Loss"] < 0])

win_rate = winners / len(df) * 100

c1, c2, c3 = st.columns(3)

c1.metric("Total Profit/Loss", f"₹{total_profit:,.0f}")
c2.metric("Winning Holdings", winners)
c3.metric("Win Rate", f"{win_rate:.1f}%")

st.divider()

# Top Winners
st.subheader("🏆 Top 10 Winners")

top_winners = df.sort_values(
    "Profit/Loss %",
    ascending=False
).head(10)

st.dataframe(
    top_winners[
        ["Name", "Current Value", "Profit/Loss", "Profit/Loss %"]
    ],
    use_container_width=True
)

# Winner Chart
fig = px.bar(
    top_winners,
    x="Name",
    y="Profit/Loss %",
    title="Top Winners (%)"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Top Losers
st.subheader("📉 Top 10 Losers")

top_losers = df.sort_values(
    "Profit/Loss %",
    ascending=True
).head(10)

st.dataframe(
    top_losers[
        ["Name", "Current Value", "Profit/Loss", "Profit/Loss %"]
    ],
    use_container_width=True
)

fig2 = px.bar(
    top_losers,
    x="Name",
    y="Profit/Loss %",
    title="Top Losers (%)"
)

st.plotly_chart(fig2, use_container_width=True)

st.divider()

# Distribution of Returns
st.subheader("📊 Return Distribution")

fig3 = px.histogram(
    df,
    x="Profit/Loss %",
    nbins=20,
    title="Portfolio Return Distribution"
)

st.plotly_chart(fig3, use_container_width=True)

st.divider()

# Largest Contributors
st.subheader("💰 Largest Profit Contributors")

contributors = df.sort_values(
    "Profit/Loss",
    ascending=False
).head(10)

fig4 = px.bar(
    contributors,
    x="Name",
    y="Profit/Loss",
    title="Largest Profit Contributors (₹)"
)

st.plotly_chart(fig4, use_container_width=True)
