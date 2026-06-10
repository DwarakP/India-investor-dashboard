import pandas as pd

def load_portfolio_data():

    equity_df = pd.read_excel("data/equity.xlsx")
    mf_df = pd.read_excel("data/mutual funds.xlsx
    invit_df = pd.read_excel("data/Bonds.xlsx")
    etf_df = pd.read_excel("data/ETF.xlsx")

    equity_df["Asset Class"] = "Indian Equity"
    mf_df["Asset Class"] = "Mutual Fund"
    invit_df["Asset Class"] = "InvIT"
    etf_df["Asset Class"] = "ETF"

    portfolio_df = pd.concat(
        [equity_df, mf_df, invit_df],
        ignore_index=True
    )

    return portfolio_df
