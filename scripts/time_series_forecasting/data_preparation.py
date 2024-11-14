import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta
import os
from utils.env_loader import load_environment


def get_db_connection():
    """
    Establishes a connection to the database.
    """
    # Load environment variables from .env file for database connection
    load_environment()
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASS')
    db_host = os.getenv('DB_HOST')
    db_name = os.getenv('DB_NAME')

    connection_string = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
    engine = create_engine(connection_string)
    return engine


def fetch_data(currency_pair='EUR/USD', look_back_days=100):
    """
    Fetches historical data from the database for a specified currency pair.

    Args:
        currency_pair (str): The currency pair to fetch data for (e.g., 'EUR/USD').
        look_back_days (int): Number of days of historical data to fetch.

    Returns:
        DataFrame: DataFrame containing historical data for the currency pair.
    """
    engine = get_db_connection()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=look_back_days)

    query = f"""
        SELECT timestamp, close
        FROM currency_data
        WHERE currency_pair = '{currency_pair}'
          AND timestamp >= '{start_date}'
          AND timestamp <= '{end_date}'
        ORDER BY timestamp ASC
    """
    data = pd.read_sql(query, engine)
    print(data)
    engine.dispose()  # Close the database connection
    return data


def scale_data(data):
    """
    Scales the 'close' prices to a range of [0, 1] using MinMaxScaler.

    Args:
        data (DataFrame): The historical currency data.

    Returns:
        scaled_data, scaler: Scaled data as a DataFrame and the scaler object.
    """
    scaler = MinMaxScaler(feature_range=(0, 1))
    data['scaled_close'] = scaler.fit_transform(data[['close']])
    return data, scaler


def prepare_data_for_lstm(data, window_size=30):
    """
    Prepares data for LSTM by creating sequences of specified window size.

    Args:
        data (DataFrame): The historical currency data with scaled values.
        window_size (int): The number of past observations to use for each sequence.

    Returns:
        X, y: Arrays for training and testing.
    """
    data_values = data['scaled_close'].values  # Using scaled 'close' values for training
    X, y = [], []
    for i in range(len(data_values) - window_size):
        X.append(data_values[i:i + window_size])
        y.append(data_values[i + window_size])
    return np.array(X), np.array(y)


def split_data(X, y, test_size=0.2):
    """
    Splits data into training and testing sets.

    Args:
        X (np.array): Array of input features.
        y (np.array): Array of target values.
        test_size (float): Fraction of the data to be used as test set.

    Returns:
        Tuple: X_train, X_test, y_train, y_test.
    """
    split_index = int(len(X) * (1 - test_size))
    X_train, X_test = X[:split_index], X[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]
    return X_train, X_test, y_train, y_test


def reshape_for_lstm(X):
    """
    Reshapes the data to be compatible with LSTM input.

    Args:
        X (np.array): Array of input features.

    Returns:
        np.array: Reshaped array with dimensions (samples, timesteps, features).
    """
    return X.reshape((X.shape[0], X.shape[1], 1))


def main():
    """
    Main function to fetch, prepare, and split data for LSTM.

    Returns:
        X_train, X_test, y_train, y_test, scaler: Prepared and split data for LSTM and scaler.
    """
    # Step 1: Fetch data
    data = fetch_data()
    print("Data fetched successfully.")

    # Step 2: Scale data
    data, scaler = scale_data(data)
    print("Data scaled successfully.")

    # Step 3: Prepare data for LSTM
    X, y = prepare_data_for_lstm(data)
    print(f"Shape of X: {X.shape}, Shape of y: {y.shape}")

    # Step 4: Split data
    X_train, X_test, y_train, y_test = split_data(X, y)
    print("Data split into training and testing sets.")

    # Step 5: Reshape data for LSTM
    X_train = reshape_for_lstm(X_train)
    X_test = reshape_for_lstm(X_test)
    print("Data reshaped for LSTM input.")

    return X_train, X_test, y_train, y_test, scaler


if __name__ == "__main__":
    X_train, X_test, y_train, y_test, scaler = main()
