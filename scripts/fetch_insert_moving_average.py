from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc
from database.db_connect import get_session
from database.schema.create_tables import CurrencyData, MovingAverage
import logging
from scripts.fetch_data import fetch_ohlc_data
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

MOVING_AVG_WINDOWS = [5, 50]  # Moving average window sizes

def get_latest_timestamp():
    """
    Fetch the latest timestamp in the currency_data table.
    """
    session = get_session()()
    try:
        latest_record = session.query(CurrencyData).order_by(desc(CurrencyData.timestamp)).first()
        if latest_record:
            return latest_record.timestamp
        return None
    finally:
        session.close()


def calculate_moving_averages(data, windows=MOVING_AVG_WINDOWS):
    """
    Calculate moving averages for each specified window size.
    """
    for window in windows:
        for i in range(window - 1, len(data)):
            window_data = data[i - window + 1:i + 1]
            moving_avg = sum(float(item['mid']['c']) for item in window_data) / window
            data[i][f"moving_avg_{window}"] = moving_avg
    return data


def insert_currency_and_moving_avg_data(data):
    session = get_session()()
    try:
        new_records = []
        moving_avg_records = []
        for record in data:
            timestamp = datetime.strptime(record['time'][:19], '%Y-%m-%dT%H:%M:%S')
            currency_data = CurrencyData(
                currency_pair="EUR/USD",
                timestamp=timestamp,
                open=float(record['mid']['o']),
                high=float(record['mid']['h']),
                low=float(record['mid']['l']),
                close=float(record['mid']['c']),
                volume=record['volume']
            )
            session.add(currency_data)
            session.flush()  # Flush to get currency_data.id for moving averages

            # Inserting moving averages for specified windows
            for window in MOVING_AVG_WINDOWS:
                if f"moving_avg_{window}" in record:
                    moving_avg_record = MovingAverage(
                        currency_data_id=currency_data.id,
                        timestamp=timestamp,
                        window_size=window,
                        moving_average=record[f"moving_avg_{window}"]
                    )
                    moving_avg_records.append(moving_avg_record)

        # Saving moving averages in bulk
        session.bulk_save_objects(moving_avg_records)
        session.commit()
        logging.info(
            f"Inserted {len(moving_avg_records)} moving average records.")

    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"Error inserting data into the database: {e}")
        raise
    finally:
        session.close()


def main():
    # Checking for the latest timestamp in the database
    latest_timestamp = get_latest_timestamp()

    if latest_timestamp:
        # Calculating the start date for fetching data as the day after the latest timestamp
        from_time = latest_timestamp + timedelta(days=1)
        data = fetch_ohlc_data(from_time=from_time)
        logging.info(f"Fetched {len(data)} new records from OANDA API starting from {from_time}")

        # Calculating moving averages and insert data into the database
        data_with_moving_avg = calculate_moving_averages(data)
        insert_currency_and_moving_avg_data(data_with_moving_avg)
    else:
        # If no data exists, fetching the initial set of data (last 100 days, for example)
        data = fetch_ohlc_data()
        data_with_moving_avg = calculate_moving_averages(data)
        insert_currency_and_moving_avg_data(data_with_moving_avg)
        logging.info(f"Fetched and inserted the initial {len(data)} records from OANDA API")


if __name__ == "__main__":
    main()
