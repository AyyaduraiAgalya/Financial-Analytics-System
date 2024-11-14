import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sqlalchemy import create_engine
import logging
from utils.env_loader import load_environment
import os

# Configure logging to output timestamp, log level, and message
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file for database connection
load_environment()
DB_USER=os.getenv('DB_USER')
DB_PASS=os.getenv('DB_PASS')
DB_HOST=os.getenv('DB_HOST')
DB_NAME=os.getenv('DB_NAME')


# Define look-back period for sequences
LOOK_BACK = 30


def load_data():
    """Load EURUSD data from the database"""
    engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}')
    query = """
        SELECT timestamp, close 
        FROM currency_data 
        WHERE currency_pair = 'EUR/USD'
        ORDER BY timestamp;
    """
    data = pd.read_sql(query, engine)
    return data

def prepare_data(data, look_back=LOOK_BACK):
    """
    Prepare data for LSTM with sequences and scaling.
    """
    # Scale data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data['close'].values.reshape(-1, 1))

    # Generate sequences
    X, y = [], []
    for i in range(look_back, len(scaled_data)):
        X.append(scaled_data[i-look_back:i, 0])  # look-back days
        y.append(scaled_data[i, 0])  # the next day
    X, y = np.array(X), np.array(y)

    return X, y, scaler

def get_X_y_scaler():
    # Load data
    data = load_data()

    # Prepare data for LSTM model
    X, y, scaler = prepare_data(data)

    print("Data preparation complete.")
    print("Shape of X:", X.shape)
    print("Shape of y:", y.shape)
    return X, y, scaler

if __name__ == "__main__":
    X, y, scaler = get_X_y_scaler()
