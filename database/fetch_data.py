import requests
import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

INSTRUMENT = "EUR_USD"
OANDA_API_URL = f"https://api-fxpractice.oanda.com/v3/instruments/{INSTRUMENT}/candles"
OANDA_API_KEY = os.getenv('OANDA_API_KEY')
GRANULARITY = "D"  # Daily candles


def fetch_ohlc_data(count=100):
    """
    Fetch OHLC data from OANDA API.

    Args:
        count (int): Number of data points to fetch.

    Returns:
        list: List of OHLC data points.
    """
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


def fetch_data():
    """
    Fetch data from OANDA API.

    Returns:
        list: List of fetched data points.
    """
    try:
        data = fetch_ohlc_data()
        logging.info(f"Fetched {len(data)} records from OANDA API")
        return data
    except Exception as e:
        logging.error(f"Error fetching data from OANDA API: {e}")
        return []


if __name__ == "__main__":
    data = fetch_data()
    print(data)
