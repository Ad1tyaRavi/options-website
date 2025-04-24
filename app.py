import plotly.express as px
from datetime import datetime
import yfinance as yf
import streamlit as st
import pandas as pd
from data_fetcher.yfinance_fetcher import YFinanceFetcher  # Correct import path
from pricing_models.black_scholes import black_scholes, calculate_historical_volatility

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

# Add to app.py
from pricing_models.black_scholes import black_scholes, calculate_historical_volatility

# In app.py
def find_mispriced_options(symbol: str, risk_free_rate: float = 0.05):
    try:
        fetcher = YFinanceFetcher()
        chain = fetcher.get_options_chain(symbol)
        if chain.empty:
            return None, None
        
        # Get current price and volatility
        stock = yf.Ticker(symbol)
        S = stock.history(period="1d")['Close'].iloc[-1]
        sigma = calculate_historical_volatility(symbol)
        
        mispricing = []
        for _, row in chain.iterrows():
            T = (row['expiration'] - pd.Timestamp.today()).days / 365
            moneyness = abs(row['strike'] - S)/S
    
            # Skip options expiring in >1 year
            if T > 1:
                continue
    
            # Skip deep OTM options (|strike - spot| > 20%)
            moneyness = abs(row['strike'] - S)/S
            if moneyness > 0.2:
                continue
            
            if pd.isna(row['bid']) or pd.isna(row['ask']) or row['bid'] <= 0 or row['ask'] <= 0:
                continue  # Skip this option
            K = row['strike']
            T = (row['expiration'] - pd.Timestamp.today()).days / 365  # Now works!
            market_price = (row['bid'] + row['ask'])/2
            if market_price < 0.05:  # Skip options priced <5 cents
                continue
            # Format theoretical prices
                theo_price = round(bs_result['price'], 2)  # Round to pennie
            option_type = 'call' if row['contractType'] == 'CALL' else 'put'
            
            if T <= 0 or market_price <= 0:
                continue
            
            theo_price = black_scholes(S, K, T, risk_free_rate, sigma, option_type)
            mispricing.append({
                'type': option_type,
                'strike': K,
                'expiration': row['expiration'].strftime('%Y-%m-%d'),
                'theoretical': theo_price,
                'market': market_price,
                'difference_pct': (theo_price - market_price)/market_price * 100
            })
        
        df = pd.DataFrame(mispricing).sort_values('difference_pct', ascending=False)
        return df.head(10), df.tail(10)
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None, None
    # Add to app.py (after existing code)
st.header("Mispriced Options Scanner")

# User inputs
col1, col2 = st.columns(2)
with col1:
    symbol = st.text_input("Enter ticker:", "SPY").upper()
with col2:
    risk_free_rate = st.number_input("Risk-Free Rate (%)", value=5.0)/100

if st.button("Find Mispriced Options"):
    overpriced, underpriced = find_mispriced_options(symbol, risk_free_rate)
    if overpriced is not None:
        st.subheader("🔥 Most Overpriced (Sell Candidates)")
        st.dataframe(overpriced.style.format({
            'theoretical': '{:.2f}',
            'market': '{:.2f}',
            'difference_pct': '{:.2f}%'
        }))
        
        st.subheader("💰 Most Underpriced (Buy Candidates)")
        st.dataframe(underpriced.style.format({
            'theoretical': '{:.2f}',
            'market': '{:.2f}',
            'difference_pct': '{:.2f}%'
        }))
        
        # Visualize discrepancies
        st.subheader("Mispricing Distribution")
        fig = px.histogram(pd.concat([overpriced, underpriced]), 
                          x='difference_pct', 
                          color='type',
                          title="Mispricing Percentage Distribution")
        st.plotly_chart(fig)


        # python -m streamlit run app.py