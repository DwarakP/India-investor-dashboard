import streamlit as st
import pandas as pd

st.title("📄 Annual Report Tracker")

st.markdown("""
Track annual reports, scores, and investment assessments.
""")

# ------------------------------------------------------------------
# Sample Data
# Later replace with annual_report_scores.csv
# ------------------------------------------------------------------

data = {
    "Company": [
        "Bajaj Holdings",
        "Schaeffler India",
        "Mastek",
        "ITC",
        "HCL Technologies"
    ],
    "FY": [
        "FY25",
        "FY25",
        "FY25",
        "FY25",
        "FY25"
    ],
    "Margin Score": [9, 8, 7, 9, 8],
    "Profitability Score": [10, 9, 8, 8, 8],
    "Cash Flow Score": [10, 8, 8, 9, 8],
    "Governance Score": [9, 8, 8, 9, 8],
    "Debt Score": [10, 8, 9, 9, 8]
}

df = pd.DataFrame(data)

# ------------------------------------------------------------------
# Overall Score
# ------------------------------------------------------------------

score_cols = [
    "Margin Score",
    "Profitability Score",
    "Cash Flow Score",
    "Governance Score",
    "Debt Score"
]

df["Overall Score"] = (
    df[score_cols].mean(axis=1)
).round(1)

# ------------------------------------------------------------------
# KPIs
# ------------------------------------------------------------------

c1, c2, c3 = st.columns(3)

c1.metric("Reports Tracked", len(df))

c2.metric(
    "Average Score",
    round(df["Overall Score"].mean(), 1)
)

c3.metric(
    "Highest Rated",
    df.sort_values(
        "Overall Score",
        ascending=False
    ).iloc[0]["Company"]
)

st.divider()

# ------------------------------------------------------------------
# Rankings
# ------------------------------------------------------------------

st.subheader("🏆 Company Rankings")

ranking = df.sort_values(
    "Overall Score",
    ascending=False
)

st.dataframe(
    ranking,
    use_container_width=True
)

st.divider()

# ------------------------------------------------------------------
# Scorecard
# ------------------------------------------------------------------

st.subheader("📊 Detailed Scorecard")

company = st.selectbox(
    "Select Company",
    df["Company"]
)

selected = df[df["Company"] == company].iloc[0]

st.write(f"### {company}")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Margin",
    selected["Margin Score"]
)

col2.metric(
    "Profitability",
    selected["Profitability Score"]
)

col3.metric(
    "Cash Flow",
    selected["Cash Flow Score"]
)

col1.metric(
    "Governance",
    selected["Governance Score"]
)

col2.metric(
    "Debt",
    selected["Debt Score"]
)

col3.metric(
    "Overall",
    selected["Overall Score"]
)

st.divider()

# ------------------------------------------------------------------
# Investment Verdict
# ------------------------------------------------------------------

st.subheader("💡 Investment Assessment")

score = selected["Overall Score"]

if score >= 9:
    st.success(
        "Excellent quality business. Strong candidate for long-term compounding."
    )
elif score >= 8:
    st.info(
        "Good quality business with manageable risks."
    )
elif score >= 7:
    st.warning(
        "Average quality. Requires closer monitoring."
    )
else:
    st.error(
        "Significant concerns identified."
    )

st.divider()

# ------------------------------------------------------------------
# Notes Section
# ------------------------------------------------------------------

st.subheader("📝 Annual Report Notes")

st.text_area(
    "Key observations",
    height=200,
    placeholder="""
Growth Drivers:
Risks:
Management Commentary:
Capital Allocation:
Valuation Thoughts:
"""
)
