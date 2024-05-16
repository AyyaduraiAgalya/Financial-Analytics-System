"""
This module handles the database connection and session creation.
"""

from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import logging

# Configure logging to output timestamp, log level, and message
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file for database connection
load_dotenv()

def get_database_url():
    """Construct the database URL from environment variables."""
    return f"postgresql+psycopg2://{os.getenv('DB_USER')}:" \
           f"{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:" \
           f"{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Initialize SQLAlchemy Engine that will manage connections
def get_engine():
    """Return the SQLAlchemy engine."""
    database_url = get_database_url()
    return create_engine(database_url, echo=True)  # echo=True enables SQL command logging

# Create a Session class bound to the engine
def get_session():
    """Return a new session."""
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()

def test_connection():
    """Test the database connection."""
    engine = get_engine()
    try:
        with engine.connect() as connection:
            logging.info("Successfully connected to the database")
    except exc.SQLAlchemyError as e:
        logging.error(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    test_connection()