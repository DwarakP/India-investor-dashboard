from utili.data_loader import load_portfolio_data

portfolio_df = load_portfolio_data()

st.dataframe(
    portfolio_df,
    use_container_width=True
)
