import streamlit as st
import pandas as pd
import plotly.express as px

st.title("⚠️ Risk Dashboard")

# Load data
df = pd.read_csv("data/Investments.csv")

# Convert numeric columns
numeric_cols = [
    "Current Value",
    "Invested Value",
    "Profit/Loss",
    "Profit/Loss %"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Portfolio weight
portfolio_value = df["Current Value"].sum()

df["Weight %"] = (
    df["Current Value"] / portfolio_value * 100
)

# KPIs
largest_position = df["Weight %"].max()
top5_concentration = (
    df.nlargest(5, "Current Value")["Weight %"].sum()
)

loss_making = len(df[df["Profit/Loss"] < 0])

c1, c2, c3 = st.columns(3)

c1.metric(
    "Largest Position",
    f"{largest_position:.2f}%"
)

c2.metric(
    "Top 5 Concentration",
    f"{top5_concentration:.2f}%"
)

c3.metric(
    "Loss-Making Holdings",
    loss_making
)

st.divider()

# Top Holdings Risk
st.subheader("📊 Position Concentration")

top10 = df.nlargest(10, "Current Value")

fig = px.bar(
    top10,
    x="Name",
    y="Weight %",
    title="Top 10 Holdings by Portfolio Weight"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Concentration Table
st.subheader("🏦 Portfolio Concentration")

st.dataframe(
    df.sort_values(
        "Weight %",
        ascending=False
    )[
        [
            "Name",
            "Current Value",
            "Weight %",
            "Profit/Loss %"
        ]
    ],
    use_container_width=True
)

st.divider()

# Loss Makers
st.subheader("🔴 Current Loss-Making Holdings")

loss_df = df[df["Profit/Loss"] < 0]

if len(loss_df) > 0:
    st.dataframe(
        loss_df[
            [
                "Name",
                "Profit/Loss",
                "Profit/Loss %"
            ]
        ].sort_values(
            "Profit/Loss %",
            ascending=True
        ),
        use_container_width=True
    )
else:
    st.success("No loss-making positions found.")

st.divider()

# Risk Categories
st.subheader("🚦 Position Risk Categories")

high_risk = len(df[df["Weight %"] > 10])
medium_risk = len(
    df[
        (df["Weight %"] > 5) &
        (df["Weight %"] <= 10)
    ]
)
low_risk = len(df[df["Weight %"] <= 5])

risk_df = pd.DataFrame({
    "Category": [
        "High Risk (>10%)",
        "Medium Risk (5%-10%)",
        "Low Risk (<5%)"
    ],
    "Count": [
        high_risk,
        medium_risk,
        low_risk
    ]
})

fig2 = px.pie(
    risk_df,
    values="Count",
    names="Category",
    title="Position Size Risk Distribution"
)

st.plotly_chart(fig2, use_container_width=True)

st.divider()

# Portfolio Health Score
st.subheader("💡 Portfolio Health")

score = 100

if largest_position > 20:
    score -= 20

if top5_concentration > 60:
    score -= 20

if loss_making > len(df) * 0.4:
    score -= 20

st.metric("Portfolio Health Score", f"{score}/100")

if score >= 80:
    st.success("Portfolio appears well diversified.")
elif score >= 60:
    st.warning("Moderate concentration risk detected.")
else:
    st.error("High concentration risk. Review allocation.")
