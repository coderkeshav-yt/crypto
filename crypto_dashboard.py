import streamlit as st
import requests
import time
import plotly.graph_objs as go

# Replace 'YOUR_API_KEY' with your actual CoinMarketCap API key
API_KEY = 'abd6121e-ec47-437b-9cd6-9fee22e91a42'  # Ensure this is your valid API key
BASE_URL = 'https://pro-api.coinmarketcap.com/v1/'

# Function to fetch cryptocurrency prices
def fetch_crypto_data(crypto):
    url = f"{BASE_URL}cryptocurrency/quotes/latest?symbol={crypto}&convert=INR"
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        return data['data'][crypto]['quote']['INR']
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from CoinMarketCap API: {e}. Please try again later.")
        return None

# Function to fetch historical price data
def fetch_historical_data(crypto):
    url = f"{BASE_URL}cryptocurrency/quotes/historical?symbol={crypto}&convert=INR&time_start=2023-10-01&time_end=2023-10-02&interval=1h"
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data['data']['quotes']
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching historical data from CoinMarketCap API: {e}.")
        return None

# List of popular cryptocurrencies
cryptos = ['BTC', 'ETH', 'DOGE', 'BNB', 'SOL', 'XRP', 'ADA', 'MATIC']

# Streamlit UI
st.set_page_config(page_title="Crypto Dashboard", page_icon="🚀", layout="centered")

# Custom CSS for styling
st.markdown("""
<style>
    body {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #ffffff;
        font-family: 'Arial', sans-serif;
    }
    .header {
        text-align: center;
        color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
        font-size: 2.5em;
    }
    .footer {
        text-align: center;
        color: #ffffff;
        padding: 10px;
        border-radius: 10px;
        position: fixed;
        bottom: 0;
        width: 100%;
    }
    .crypto-card {
        background-color: #2e2e2e;
        border-radius: 10px;
        padding: 15px;
        margin: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        transition: transform 0.2s;
    }
    .crypto-card:hover {
        transform: scale(1.05);
    }
    .crypto-price {
        font-size: 24px;
        color: #00ff00;
        margin-left: auto;
    }
    .selectbox {
        background-color: #2e2e2e;
        color: #ffffff;
        border: none;
        border-radius: 5px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<div class='header'><h1>Live Cryptocurrency Dashboard 🚀</h1></div>", unsafe_allow_html=True)
st.markdown("Select a cryptocurrency to see its real-time price in INR.")

# Dropdown menu for cryptocurrency selection
selected_crypto = st.selectbox("Choose a cryptocurrency:", cryptos)

# Display loading spinner
with st.spinner("Fetching data..."):
    if selected_crypto:
        crypto_data = fetch_crypto_data(selected_crypto)
        historical_data = fetch_historical_data(selected_crypto)

        if crypto_data:
            # Display cryptocurrency card
            st.markdown(f"<div class='crypto-card'>{selected_crypto} <span class='crypto-price'>₹{crypto_data['price']}</span></div>", unsafe_allow_html=True)
            
            # Check for keys before accessing them
            market_cap = crypto_data.get('market_cap', 'N/A')
            change_24h = crypto_data.get('percent_change_24h', 'N/A')
            volume = crypto_data.get('volume_24h', 'N/A')

            st.markdown(f"<div class='crypto-card'>Market Cap: ₹{market_cap} | 24h Change: {change_24h}% | Volume: ₹{volume}</div>", unsafe_allow_html=True)

            # Plot historical price data
            if historical_data:
                prices = [quote['quote']['INR']['price'] for quote in historical_data]
                timestamps = [quote['time_open'] for quote in historical_data]

                fig = go.Figure()
                fig.add_trace(go.Scatter(x=timestamps, y=prices, mode='lines', name='Price', line=dict(color='green')))
                fig.update_layout(title=f'{selected_crypto} Price Trend (Last 24 Hours)',
                                  xaxis_title='Time',
                                  yaxis_title='Price in INR',
                                  xaxis=dict(showgrid=False),
                                  yaxis=dict(showgrid=False),
                                  plot_bgcolor='rgba(0,0,0,0)',
                                  paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig)

# Real-time updates every 30 seconds
while True:
    time.sleep(30)  # Increased interval to 30 seconds
    if selected_crypto:
        with st.spinner("Fetching updated data..."):
            crypto_data = fetch_crypto_data(selected_crypto)
            historical_data = fetch_historical_data(selected_crypto)

            if crypto_data:
                st.markdown(f"<div class='crypto-card'>{selected_crypto} <span class='crypto-price'>₹{crypto_data['price']}</span></div>", unsafe_allow_html=True)
                
                # Check for keys before accessing them
                market_cap = crypto_data.get('market_cap', 'N/A')
                change_24h = crypto_data.get('percent_change_24h', 'N/A')
                volume = crypto_data.get('volume_24h', 'N/A')

                st.markdown(f"<div class='crypto-card'>Market Cap: ₹{market_cap} | 24h Change: {change_24h}% | Volume: ₹{volume}</div>", unsafe_allow_html=True)

                # Plot historical price data
                if historical_data:
                    prices = [quote['quote']['INR']['price'] for quote in historical_data]
                    timestamps = [quote['time_open'] for quote in historical_data]

                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=timestamps, y=prices, mode='lines', name='Price', line=dict(color='green')))
                    fig.update_layout(title=f'{selected_crypto} Price Trend (Last 24 Hours)',
                                      xaxis_title='Time',
                                      yaxis_title='Price in INR',
                                      xaxis=dict(showgrid=False),
                                      yaxis=dict(showgrid=False),
                                      plot_bgcolor='rgba(0,0,0,0)',
                                      paper_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig)

# Footer
st.markdown("<div class='footer'>Made with ❤️ by Your Name | <a href='https://www.coinmarketcap.com/' style='color: #00ff00;'>CoinMarketCap</a></div>", unsafe_allow_html=True)
