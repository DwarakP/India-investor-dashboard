import pandas as pd
import streamlit as st

@st.cache_data
def load_portfolio():
    return pd.read_csv("data/Investments.csv")

def load_css():
    try:
        with open("assets/style.css") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )
    except:
        pass
