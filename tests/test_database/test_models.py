import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.db_connect import Base
from database.schema.models import CurrencyData, MovingAverage, Prediction
from datetime import datetime

class TestModels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up an in-memory SQLite database for testing
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        # Create a new session for each test
        self.session = self.Session()

    def tearDown(self):
        # Roll back any changes made during the test
        self.session.rollback()
        self.session.close()

    def test_currency_data_model(self):
        # Test inserting and querying CurrencyData
        data = CurrencyData(
            currency_pair='EUR/USD',
            timestamp=datetime.now(),
            open=1.2,
            high=1.3,
            low=1.1,
            close=1.25,
            volume=1000
        )
        self.session.add(data)
        self.session.commit()

        # Query the database to check if the record was inserted
        result = self.session.query(CurrencyData).first()
        self.assertIsNotNone(result)
        self.assertEqual(result.currency_pair, 'EUR/USD')

    def test_moving_average_model(self):
        # Test inserting and querying MovingAverage
        currency_data = CurrencyData(
            currency_pair='EUR/USD',
            timestamp=datetime.now(),
            open=1.2,
            high=1.3,
            low=1.1,
            close=1.25,
            volume=1000
        )
        self.session.add(currency_data)
        self.session.commit()

        ma = MovingAverage(
            currency_data_id=currency_data.id,
            timestamp=datetime.now(),
            window_size=5,
            moving_average=1.23
        )
        self.session.add(ma)
        self.session.commit()

        # Query the database to check if the record was inserted
        result = self.session.query(MovingAverage).first()
        self.assertIsNotNone(result)
        self.assertEqual(result.window_size, 5)

    def test_prediction_model(self):
        # Test inserting and querying Prediction
        currency_data = CurrencyData(
            currency_pair='EUR/USD',
            timestamp=datetime.now(),
            open=1.2,
            high=1.3,
            low=1.1,
            close=1.25,
            volume=1000
        )
        self.session.add(currency_data)
        self.session.commit()

        prediction = Prediction(
            currency_data_id=currency_data.id,
            timestamp=datetime.now(),
            model_name='LinearRegression',
            predicted_close=1.26
        )
        self.session.add(prediction)
        self.session.commit()

        # Query the database to check if the record was inserted
        result = self.session.query(Prediction).first()
        self.assertIsNotNone(result)
        self.assertEqual(result.model_name, 'LinearRegression')

if __name__ == '__main__':
    unittest.main()
