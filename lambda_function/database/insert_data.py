"""
This module handles the insertion of currency data into the database.
"""

from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from database.db_connect import get_session
from database.schema.create_tables import CurrencyData
from scripts.fetch_data import fetch_data
import logging

def record_exists(session, currency_pair, timestamp):
    """
    Check if a record already exists in the database.

    Args:
        session (Session): SQLAlchemy session object.
        currency_pair (str): The currency pair (e.g., 'EUR/USD').
        timestamp (datetime): The timestamp of the record.

    Returns:
        bool: True if the record exists, False otherwise.
    """
    return session.query(CurrencyData).filter_by(currency_pair=currency_pair, timestamp=timestamp).first() is not None

def create_currency_data_record(record):
    """
    Create a CurrencyData record from raw data.

    Args:
        record (dict): A dictionary containing raw data for a single record.

    Returns:
        CurrencyData: An instance of CurrencyData populated with the provided data.
    """
    time_str = record['time'][:26] + 'Z'
    timestamp = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    return CurrencyData(
        currency_pair='EUR/USD',
        timestamp=timestamp,
        open=float(record['mid']['o']),
        high=float(record['mid']['h']),
        low=float(record['mid']['l']),
        close=float(record['mid']['c']),
        volume=record['volume']
    )

def insert_currency_data(data):
    """
    Insert fetched currency data into the database.

    Args:
        data (list): List of currency data points to insert.
    """
    Session = get_session()
    session = Session()
    try:
        new_records = []
        for record in data:
            # Create record and check if it exists
            currency_data = create_currency_data_record(record)
            if not record_exists(session, currency_data.currency_pair, currency_data.timestamp):
                new_records.append(currency_data)
            else:
                logging.info(f"Record already exists for timestamp {currency_data.timestamp}")

        if new_records:
            session.bulk_save_objects(new_records)
            session.commit()
            logging.info(f"Inserted {len(new_records)} new records into the database")
        else:
            logging.info("No new records to insert")

    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"Error inserting data into the database: {e}")
        raise  # Re-raise the exception to ensure it can be caught by tests
    finally:
        session.close()

if __name__ == "__main__":
    data = fetch_data()
    insert_currency_data(data)
