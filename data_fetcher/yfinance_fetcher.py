import yfinance as yf
import pandas as pd
from .base_fetcher import BaseDataFetcher

class YFinanceFetcher(BaseDataFetcher):
    def get_options_chain(self, symbol: str):
        try:
            stock = yf.Ticker(symbol)
            chain = stock.options_chain
            # Combine calls and puts into one DataFrame
            return pd.concat([chain.calls, chain.puts])
        except Exception as e:
            return pd.DataFrame()  # Return empty if error