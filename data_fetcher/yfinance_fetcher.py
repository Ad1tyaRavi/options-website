import yfinance as yf
import pandas as pd
from .base_fetcher import BaseDataFetcher  # Fix: Relative import

class YFinanceFetcher(BaseDataFetcher):
    def get_options_chain(self, symbol: str):
        try:
            stock = yf.Ticker(symbol)
            expirations = stock.options  # Check if options exist
            if not expirations:
                print(f"No options for {symbol}")
                return pd.DataFrame()
            
            # Fetch the nearest expiration
            nearest_expiry = expirations[0]
            chain = stock.option_chain(nearest_expiry)  # Correct method name
            
            # Combine calls and puts
            combined = pd.concat([chain.calls, chain.puts])
            return combined
        except Exception as e:
            print(f"Error: {e}")
            return pd.DataFrame()