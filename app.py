import streamlit as st
import pandas as pd
from data_fetcher.yfinance_fetcher import YFinanceFetcher  # Correct import path

fetcher = YFinanceFetcher()

st.title("Options Chain Viewer")
symbol = st.text_input("Enter Ticker (e.g., SPY):", "SPY").upper().strip()

if symbol:
    st.write(f"Fetching data for **{symbol}**...")
    chain = fetcher.get_options_chain(symbol)
    
    if not chain.empty:
        st.dataframe(chain)
    else:
        st.error("No data found. Try a different ticker (e.g., SPY, AAPL).")