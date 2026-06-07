import streamlit as st
import pandas as pd
import plotly.express as px

from utils import load_css

load_css()

st.title("📉 Portfolio vs Nifty 500")

# --------------------------------------------------
# Load Data
# --------------------------------------------------

portfolio = pd.read_csv(
    "data/portfolio_history.csv"
)

benchmark = pd.read_csv(
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
# KPI Calculations
# --------------------------------------------------

current_portfolio_value = df["Portfolio_Value"].iloc[-1]

portfolio_cr = current_portfolio_value / 10000000

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

winning_months = (df["Alpha"] > 0).sum()

# --------------------------------------------------
# KPI Row 1
# --------------------------------------------------

row1_col1, row1_col2, row1_col3 = st.columns(3)

row1_col1.metric(
    "Portfolio Value",
    f"₹{portfolio_cr:.2f} Cr"
)

row1_col2.metric(
    "Portfolio Return",
    f"{portfolio_return:.2f}%"
)

row1_col3.metric(
    "Nifty 500 Return",
    f"{benchmark_return:.2f}%"
)

# --------------------------------------------------
# KPI Row 2
# --------------------------------------------------

row2_col1, row2_col2 = st.columns(2)

row2_col1.metric(
    "Alpha Generated",
    f"{alpha:.2f}%"
)

row2_col2.metric(
    "Winning Months",
    f"{winning_months}/{len(df)-1}"
)

st.divider()



# Latest month values

latest_portfolio_return = df["Portfolio_Return"].iloc[-1]

latest_benchmark_return = df["Benchmark_Return"].iloc[-1]

latest_alpha = (
    latest_portfolio_return
    - latest_benchmark_return
)
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
