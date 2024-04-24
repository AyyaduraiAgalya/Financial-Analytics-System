import requests
import pandas as pd
from dotenv import load_dotenv
import os
import logging


# Function to fetch EUR/USD data from OANDA API.
def fetch_forex_data(api_key):
    """Fetches and returns historical daily forex data for EUR/USD from the OANDA API.

    Args:
        api_key (str): OANDA API key for authorization.

    Returns:
        pd.DataFrame: Dataframe containing the time and close prices for EUR/USD.
    """
    # Define the API endpoint and set necessary headers and query parameters
    url = "https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles"
    headers = {'Authorization':f'Bearer {api_key}'}
    params = {
        'count': 500, # Number of data points to fetch
        'granularity': 'D' # Daily data
    }

    # Make the API request and parse the response into JSON
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        logging.error(f'Error fetching data:{e}')
        return None

    # Extract prices and times into a DataFrame
    prices = [{'time': x['time'], 'close': x['mid']['c']} for x in data['candles']]

    # Convert the list of prices to a DataFrame, convert time to datetime, and set as index
    df = pd.DataFrame(prices)
    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)

    return df


# Basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Main section to run if script is executed directly
if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file
    api_key = os.getenv('OANDA_API_KEY')  # Replace 'OANDA_API_KEY' with your actual OANDA API key stored in the .env file
    eurusd_data = fetch_forex_data(api_key)
    if eurusd_data is not None:
        logging.info(f'\n{eurusd_data.head()}')

