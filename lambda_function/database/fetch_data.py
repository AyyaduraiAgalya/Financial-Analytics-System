import requests
import os
from utils.env_loader import load_environment
import logging

# Load environment variables
load_environment()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Constant - Daily value of currency_pair
GRANULARITY = "D"


def fetch_ohlc_data(instrument, count=100):
    """
    Fetch OHLC data from OANDA API.

    Args:
        instrument (str): The currency pair to fetch data for
        count (int): Number of data points to fetch.

    Returns:
        list: List of OHLC data points.
    """
    OANDA_API_KEY = os.getenv('OANDA_API_KEY')
    if not OANDA_API_KEY:
        raise ValueError("OANDA_API_KEY environment variable not set")

    OANDA_API_URL = f"https://api-fxpractice.oanda.com/v3/instruments/{instrument}/candles"
    headers = {
        "Authorization": f"Bearer {OANDA_API_KEY}"
    }
    params = {
        "count": count,
        "granularity": GRANULARITY
    }
    response = requests.get(OANDA_API_URL, headers=headers, params=params)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()["candles"]


def fetch_data(currency_pair="EUR_USD"):
    """
    Fetch data from OANDA API.

    Args:
        currency_pair (str): The currency pair to fetch data for.

    Returns:
        list: List of fetched data points.
    """
    try:
        data = fetch_ohlc_data(currency_pair)
        logging.info(f"Fetched {len(data)} records from OANDA API")
        return data
    except Exception as e:
        logging.error(f"Error fetching data from OANDA API: {e}")
        return []


if __name__ == "__main__":
    # For local testing, ensure the environment variable is set
    os.environ['OANDA_API_KEY'] = os.getenv('OANDA_API_KEY')
    data = fetch_data()
    print(data)
