"""
This module handles fetching forex data EURUSD and basic cleaning of the data
"""

import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout
import pandas as pd
from dotenv import load_dotenv
import os
import logging

# Function to fetch EUR/USD data from OANDA API
def fetch_forex_data(api_key):
    """Fetches and returns historical daily forex data for EUR/USD from the OANDA API.

        Args:
            api_key (str): OANDA API key for authorisation.

        Returns:
            pd.DataFrame: Dataframe containing the time and close prices for EUR/USD.
        """
    # Defining the API endpoint and set necessary headers and query parameters
    url = "https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles"
    headers = {'Authorization': f'Bearer {api_key}'}
    params = {
        'count': 500,
        'granularity': 'D'
    }

    # Making the API request and parse the response into JSON
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Will raise an exception for HTTP errors
        data = response.json()
    except HTTPError as http_err:
        # Handling specific HTTP errors based on status codes
        status_code = http_err.response.status_code
        if status_code == 400:
            logging.error('Bad Request - Check your query parameters.')
        elif status_code == 401:
            logging.error('Unauthorized - Check your API key or authentication details.')
        else:
            logging.error(f'HTTP error occurred: {http_err}')
        return None
    except (ConnectionError, Timeout) as conn_err:
        logging.error(f'Network error: {conn_err}')
        return None
    except Exception as err:
        logging.error(f'An error occurred: {err}')
        return None

    # Extracting prices and times into a DataFrame
    prices = [{'time': x['time'], 'close': x['mid']['c']} for x in data['candles']]

    # Converting the list of prices to a DataFrame,
    df = pd.DataFrame(prices)


    # Ensuring 'close' is a float
    df['close'] = pd.to_numeric(df['close'], errors='coerce')

    # Converting time to datetime, and set as index
    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)

    return df


def clean_data(df):
    """Cleans the fetched EURUSD data.

    Args:
        df (pd.DataFrame): The DataFrame containing EURUSD data.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """

    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True) # Drop rows with any missing values

    return df

# Basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Main section to run if script is executed directly
if __name__ == "__main__":
    load_dotenv()  # Loading environment variables from .env file
    api_key = os.getenv('OANDA_API_KEY')  # 'OANDA_API_KEY' will be your actual OANDA API key stored in the .env file as per the setup instructions
    eurusd_data = fetch_forex_data(api_key)
    if eurusd_data is not None:
        eurusd_data = clean_data(eurusd_data)
        logging.info(f'\n{eurusd_data.head()}')

