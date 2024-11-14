import requests
import os
from utils.env_loader import load_environment
import logging

# Loading environment variables
load_environment()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Constants
OANDA_API_KEY = os.getenv("OANDA_API_KEY")
OANDA_API_URL = "https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles"
GRANULARITY = "D"  # Daily data

def fetch_ohlc_data(instrument="EUR_USD", from_time=None, count=100):
    headers = {"Authorization": f"Bearer {OANDA_API_KEY}"}
    params = {"granularity": GRANULARITY, "count": count}

    # Formatting the from_time to ISO 8601 (UTC with 'Z' at the end, no offsets)
    if from_time:
        # Set time to midnight UTC for daily data and format it properly
        from_time_utc = from_time.replace(hour=0, minute=0, second=0, microsecond=0)
        params["from"] = from_time_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
        print(f"Fetching data from {params['from']}")  # Debug print statement

    try:
        response = requests.get(OANDA_API_URL, headers=headers, params=params)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Request URL was: {response.url}")
        raise
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

