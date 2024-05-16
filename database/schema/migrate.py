import logging
from database.db_connect import get_engine, Base
from database.schema.models import CurrencyData, MovingAverage, Prediction  # Import the models

def migrate_database():
    """
    Migrate the database schema.

    This function initializes the database schema based on the defined models
    by creating the necessary tables.
    """
    engine = get_engine()
    Base.metadata.create_all(engine)
    logging.info("Database schema created successfully")

if __name__ == "__main__":
    migrate_database()
