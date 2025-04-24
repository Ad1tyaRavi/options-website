# data_fetcher/yfinance_fetcher.py
import yfinance as yf
import pandas as pd
from .base_fetcher import BaseDataFetcher

class YFinanceFetcher(BaseDataFetcher):
    def get_options_chain(self, symbol: str):
        try:
            stock = yf.Ticker(symbol)
            expirations = stock.options
            if not expirations:
                return pd.DataFrame()
            
            # Fetch nearest expiration
            nearest_expiry = expirations[0]
            chain = stock.option_chain(nearest_expiry)
            
            # Add expiration and contract type columns
            chain.calls['expiration'] = pd.Timestamp(nearest_expiry)  # Convert to Timestamp
            chain.calls['contractType'] = 'CALL'
            chain.puts['expiration'] = pd.Timestamp(nearest_expiry)
            chain.puts['contractType'] = 'PUT'
            
            # Combine calls and puts
            combined = pd.concat([chain.calls, chain.puts])
            return combined
        except Exception as e:
            print(f"Error: {e}")
            return pd.DataFrame()