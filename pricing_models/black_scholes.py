# pricing_models/black_scholes.py
import yfinance as yf
import numpy as np
from scipy.stats import norm
from typing import Dict

def black_scholes(S: float, K: float, T: float, r: float, sigma: float, option_type: str) -> float:
    """
    Calculate Black-Scholes option price.
    """
    if T <= 0 or sigma <= 0:
        return 0.0  # Handle expired/instant expiration
    
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    
    if option_type == 'call':
        price = S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
    else:
        price = K*np.exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)
    return price

def calculate_historical_volatility(ticker: str, window: int = 30) -> float:
    """
    Compute annualized historical volatility from daily returns.
    """
    stock = yf.Ticker(ticker)
    hist = stock.history(period=f"{window}d")
    returns = np.log(hist['Close']/hist['Close'].shift(1))
    return returns.std() * np.sqrt(252)  # Annualized