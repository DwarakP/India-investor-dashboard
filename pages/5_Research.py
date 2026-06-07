import streamlit as st
import pandas as pd

st.title("📚 Research Hub")

st.markdown("""
Store investment ideas, annual report notes,
sector themes and company research.
""")

# -------------------------
# Investment Checklist
# -------------------------

st.subheader("✅ Investment Checklist")

checklist = [
    "Revenue growth > 10%",
    "ROCE > 15%",
    "Debt under control",
    "Positive Free Cash Flow",
    "Promoter holding stable",
    "No major governance issues",
    "Reasonable valuation"
]

for item in checklist:
    st.checkbox(item)

st.divider()

# -------------------------
# Investment Thesis
# -------------------------

st.subheader("📝 Investment Thesis")

st.text_area(
    "Write your investment thesis",
    height=200,
    placeholder="""
Example:

Company:
Reason for investment:
Growth drivers:
Risks:
Target allocation:
"""
)

st.divider()

# -------------------------
# Theme Tracker
# -------------------------

st.subheader("⚡ Theme Tracker")

themes = {
    "Data Centres": [
        "CG Power",
        "Hitachi Energy India",
        "GE Vernova T&D India",
        "Power Grid",
        "Blue Star"
    ],
    "Power": [
        "NTPC",
        "Power Grid",
        "Tata Power"
    ],
    "Defence": [
        "BEL",
        "HAL",
        "Bharat Dynamics"
    ],
    "EMS": [
        "Kaynes",
        "Dixon",
        "Syrma SGS"
    ]
}

selected_theme = st.selectbox(
    "Select Theme",
    list(themes.keys())
)

for stock in themes[selected_theme]:
    st.write(f"• {stock}")

st.divider()

# -------------------------
# Research Notes
# -------------------------

st.subheader("📄 Research Notes")

notes = st.text_area(
    "Meeting Notes / Annual Report Notes",
    height=300
)

st.divider()

# -------------------------
# Watchlist
# -------------------------

st.subheader("🎯 Watchlist Ideas")

watchlist = pd.DataFrame({
    "Company": [
        "CG Power",
        "Hitachi Energy",
        "Mastek",
        "Bajaj Holdings"
    ],
    "Status": [
        "Tracking",
        "Researching",
        "Accumulating",
        "Holding"
    ]
})

st.dataframe(
    watchlist,
    use_container_width=True
)
