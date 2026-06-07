import streamlit as st
import pandas as pd
import plotly.express as px

from utils import load_css

load_css()

st.title("📉 Portfolio vs Nifty 500")

# --------------------------------------------------
# Load Data
# --------------------------------------------------

portfolio = pd.read_excel(
    "data/portfolio_history.csv"
)

benchmark = pd.read_excel(
    "data/nifty500_history.csv"
)

portfolio["Date"] = pd.to_datetime(portfolio["Date"])
benchmark["Date"] = pd.to_datetime(benchmark["Date"])

# --------------------------------------------------
# Merge
# --------------------------------------------------

df = pd.merge(
    portfolio,
    benchmark,
    on="Date",
    how="inner"
)

# --------------------------------------------------
# Returns
# --------------------------------------------------

df["Portfolio_Return"] = (
    df["Portfolio_Value"].pct_change() * 100
)

df["Benchmark_Return"] = (
    df["Nifty500"].pct_change() * 100
)

df["Alpha"] = (
    df["Portfolio_Return"]
    - df["Benchmark_Return"]
)

# --------------------------------------------------
# Growth of 100
# --------------------------------------------------

df["Portfolio_Growth"] = (
    df["Portfolio_Value"]
    / df["Portfolio_Value"].iloc[0]
) * 100

df["Benchmark_Growth"] = (
    df["Nifty500"]
    / df["Nifty500"].iloc[0]
) * 100

# --------------------------------------------------
# KPIs
# --------------------------------------------------

portfolio_return = (
    (
        df["Portfolio_Value"].iloc[-1]
        / df["Portfolio_Value"].iloc[0]
    ) - 1
) * 100

benchmark_return = (
    (
        df["Nifty500"].iloc[-1]
        / df["Nifty500"].iloc[0]
    ) - 1
) * 100

alpha = portfolio_return - benchmark_return

best_month = (
    df.loc[
        df["Portfolio_Return"].idxmax(),
        "Date"
    ].strftime("%b %Y")
)

worst_month = (
    df.loc[
        df["Portfolio_Return"].idxmin(),
        "Date"
    ].strftime("%b %Y")
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Portfolio Return",
    f"{portfolio_return:.2f}%"
)

c2.metric(
    "Nifty 500 Return",
    f"{benchmark_return:.2f}%"
)

c3.metric(
    "Alpha",
    f"{alpha:.2f}%"
)

c4.metric(
    "Best Month",
    best_month
)

st.divider()

# --------------------------------------------------
# Growth of 100
# --------------------------------------------------

st.subheader("📈 Growth of ₹100")

growth = df[
    [
        "Date",
        "Portfolio_Growth",
        "Benchmark_Growth"
    ]
].melt(
    id_vars="Date",
    var_name="Series",
    value_name="Value"
)

fig = px.line(
    growth,
    x="Date",
    y="Value",
    color="Series",
    markers=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Portfolio Value Trend
# --------------------------------------------------

st.subheader("💰 Portfolio Value")

fig2 = px.line(
    df,
    x="Date",
    y="Portfolio_Value",
    markers=True
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# --------------------------------------------------
# Monthly Return Comparison
# --------------------------------------------------

st.subheader("📊 Monthly Returns")

returns = df[
    [
        "Date",
        "Portfolio_Return",
        "Benchmark_Return"
    ]
].copy()

returns["Month"] = (
    returns["Date"]
    .dt.strftime("%b-%y")
)

returns = returns.dropna()

fig3 = px.bar(
    returns,
    x="Month",
    y=[
        "Portfolio_Return",
        "Benchmark_Return"
    ],
    barmode="group"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# --------------------------------------------------
# Alpha Trend
# --------------------------------------------------

st.subheader("🚀 Monthly Alpha")

fig4 = px.bar(
    returns.assign(
        Alpha=
        returns["Portfolio_Return"]
        - returns["Benchmark_Return"]
    ),
    x="Month",
    y="Alpha"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# --------------------------------------------------
# Detailed Table
# --------------------------------------------------

st.subheader("📋 Monthly Performance Table")

table = df[
    [
        "Date",
        "Portfolio_Value",
        "Portfolio_Return",
        "Nifty500",
        "Benchmark_Return",
        "Alpha"
    ]
]

st.dataframe(
    table.round(2),
    use_container_width=True
)
