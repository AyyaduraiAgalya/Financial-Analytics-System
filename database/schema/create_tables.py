from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.db_connect import Base


class CurrencyData(Base):
    """
    Represents currency data.

    Attributes:
        id (int): Primary key.
        currency_pair (str): The currency pair (e.g., EUR/USD).
        timestamp (datetime): The timestamp of the data.
        open (float): The opening price.
        high (float): The highest price.
        low (float): The lowest price.
        close (float): The closing price.
        volume (float): The volume of trading.
    """
    __tablename__ = 'currency_data'

    id = Column(Integer, primary_key=True)
    currency_pair = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)

    moving_averages = relationship('MovingAverage', back_populates='currency_data')
    predictions = relationship('Prediction', back_populates='currency_data')


class MovingAverage(Base):
    """
    Represents a moving average.

    Attributes:
        id (int): Primary key.
        currency_data_id (int): Foreign key to currency data.
        timestamp (datetime): The timestamp of the moving average.
        window_size (int): The size of the moving average window.
        moving_average (float): The moving average value.
    """
    __tablename__ = 'moving_average'

    id = Column(Integer, primary_key=True)
    currency_data_id = Column(Integer, ForeignKey('currency_data.id'), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    window_size = Column(Integer, nullable=False)
    moving_average = Column(Float, nullable=False)

    currency_data = relationship('CurrencyData', back_populates='moving_averages')


class Prediction(Base):
    """
    Represents a prediction.

    Attributes:
        id (int): Primary key.
        currency_data_id (int): Foreign key to currency data.
        timestamp (datetime): The timestamp of the prediction.
        model_name (str): The name of the model used for prediction.
        predicted_close (float): The predicted closing price.
    """
    __tablename__ = 'prediction'

    id = Column(Integer, primary_key=True)
    currency_data_id = Column(Integer, ForeignKey('currency_data.id'), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    model_name = Column(String, nullable=False)
    predicted_close = Column(Float, nullable=False)

    currency_data = relationship('CurrencyData', back_populates='predictions')
