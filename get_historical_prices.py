import requests
import pandas as pd
import os
import requests
import pandas as pd

# Fetch tokens from CoinMarketCap
def fetch_top_erc20_tokens_from_coinmarketcap(limit=50):
    api_key = os.getenv('COINMARKETCAP_API_KEY')  # Fetch the API key from environment variables
    
    if not api_key:
        raise Exception("API key not found. Please set the COINMARKETCAP_API_KEY environment variable.")
    
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }
    params = {
        'start': '1',
        'limit': '200',  # Fetch a larger number and then filter down to ERC-20 tokens
        'convert': 'USD',
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    # Check if the response was successful
    if response.status_code != 200:
        raise Exception(f"Error fetching data from CoinMarketCap API: {response.status_code}, {response.text}")
    
    data = response.json()
    
    # Check if 'data' key is in the JSON response
    if 'data' not in data:
        raise KeyError("'data' key not found in the API response")
    
    # Extract ERC-20 tokens and ETH
    erc20_tokens = []
    eth_token = None
    for token in data['data']:
        if token['symbol'] == 'ETH':
            eth_token = token
        else:
            erc20_tokens.append(token)
    
    # Ensure ETH is always included in the list
    if eth_token:
        erc20_tokens.insert(0, eth_token)
    
    # Sort by market cap to get the top `limit` tokens, ensuring ETH is always included
    erc20_tokens = sorted(erc20_tokens, key=lambda x: x['quote']['USD']['market_cap'], reverse=True)
    erc20_tokens = erc20_tokens[:limit]
    
    # Convert to DataFrame
    df = pd.DataFrame(erc20_tokens)
    
    return df

# Construct the list objec
top_tokens = fetch_top_erc20_tokens_from_coinmarketcap()

from binance import Client
import pandas as pd
from datetime import datetime
import time

# Initialize the Binance client
# Replace 'YOUR_API_KEY' and 'YOUR_API_SECRET' with your actual Binance API key and secret
client = Client(api_key='bucKUSO8lvKBoUgg9Fjs9VvPK8S6vgiONoKYeJFVOQKxVWIbSQzzwuC7i9x8KBwb', api_secret='PWQ3HY0uPRNnLzOC28W5CFca6iqokcMDDbae3wBrcDNIfRMlQ3XaI7YwtcduTqnB')

# Define the function to get historical data
def get_historical_data(symbol, start_date):
    start_str = start_date.strftime('%d %b %Y %H:%M:%S')
    klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, start_str)
    data = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume', 
        'close_time', 'quote_asset_volume', 'number_of_trades', 
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    data.set_index('timestamp', inplace=True)
    data = data[['close']].astype(float)
    return data

# Initialize dictionary to store data
aux = {}

# Fetch historical data for each symbol
for symbol in top_tokens.symbol:
    try:
        historical_data = get_historical_data(symbol+'USDT', datetime(2023, 1, 1))
        aux[symbol] = historical_data['close']
        time.sleep(1)  # Sleep to avoid hitting API rate limits
    except Exception as e:
        print(f"Error retrieving data for {symbol}: {e}")

# Convert dictionary to DataFrame
df = pd.DataFrame(aux)

df.to_csv('historical_prices.csv', index=False)