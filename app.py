import streamlit as st
import pandas as pd
from data_fetcher.yfinance_fetcher import YFinanceFetcher

# Initialize the data fetcher
fetcher = YFinanceFetcher()

# Set up the webpage
st.title("📊 Options Chain Viewer")
symbol = st.text_input("Enter a stock ticker (e.g., AAPL):", "AAPL").upper()

if symbol:
    st.write(f"Fetching options chain for **{symbol}**...")
    chain = fetcher.get_options_chain(symbol)
    if not chain.empty:
        st.dataframe(chain)  # Show the data in a table
    else:
        st.error("Failed to fetch data. Check the ticker or try again later.")