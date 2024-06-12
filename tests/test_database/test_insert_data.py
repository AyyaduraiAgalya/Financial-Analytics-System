import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from database.insert_data import record_exists, create_currency_data_record, insert_currency_data
from database.schema.create_tables import CurrencyData
import logging

class TestInsertData(unittest.TestCase):

    @patch('database.insert_data.CurrencyData')
    def test_record_exists(self, mock_CurrencyData):
        """Test if record_exists correctly checks for an existing record."""
        mock_session = MagicMock()
        mock_query = mock_session.query.return_value
        mock_filter = mock_query.filter_by.return_value

        # Test case where record does not exist
        mock_filter.first.return_value = None
        result = record_exists(mock_session, 'EUR/USD', datetime.now())
        self.assertFalse(result)

        # Test case where record exists
        mock_filter.first.return_value = True
        result = record_exists(mock_session, 'EUR/USD', datetime.now())
        self.assertTrue(result)

    def test_create_currency_data_record(self):
        """Test if create_currency_data_record creates a CurrencyData instance correctly."""
        record = {
            'time': '2023-05-01T15:45:30.123456Z',
            'mid': {'o': '1.1000', 'h': '1.2000', 'l': '1.0500', 'c': '1.1500'},
            'volume': 1000
        }
        currency_data = create_currency_data_record(record)

        self.assertIsInstance(currency_data, CurrencyData)
        self.assertEqual(currency_data.currency_pair, 'EUR/USD')
        self.assertEqual(currency_data.timestamp, datetime.strptime('2023-05-01T15:45:30.123456Z', '%Y-%m-%dT%H:%M:%S.%fZ'))
        self.assertEqual(currency_data.open, 1.1000)
        self.assertEqual(currency_data.high, 1.2000)
        self.assertEqual(currency_data.low, 1.0500)
        self.assertEqual(currency_data.close, 1.1500)
        self.assertEqual(currency_data.volume, 1000)

    @patch('database.insert_data.get_session')
    @patch('database.insert_data.create_currency_data_record')
    @patch('database.insert_data.record_exists')
    def test_insert_currency_data(self, mock_record_exists, mock_create_currency_data_record, mock_get_session):
        """Test if insert_currency_data correctly inserts new currency data."""
        mock_session = MagicMock()
        mock_get_session.return_value = MagicMock(return_value=mock_session)

        # Mock data
        data = [{'time': '2023-05-01T15:45:30.123456Z', 'mid': {'o': '1.1000', 'h': '1.2000', 'l': '1.0500', 'c': '1.1500'}, 'volume': 1000}]
        currency_data_mock = MagicMock()
        mock_create_currency_data_record.return_value = currency_data_mock

        # Test case where record does not exist
        mock_record_exists.return_value = False
        insert_currency_data(data)
        mock_session.bulk_save_objects.assert_called_once_with([currency_data_mock])
        mock_session.commit.assert_called_once()
        mock_session.close.assert_called_once()

        # Reset mocks for next test
        mock_session.reset_mock()
        mock_record_exists.reset_mock()
        mock_record_exists.return_value = True

        # Test case where record exists
        insert_currency_data(data)
        mock_session.bulk_save_objects.assert_not_called()
        mock_session.commit.assert_not_called()
        mock_session.close.assert_called_once()

    @patch('database.insert_data.get_session')
    @patch('database.insert_data.create_currency_data_record')
    @patch('database.insert_data.record_exists')
    def test_insert_currency_data_with_exception(self, mock_record_exists, mock_create_currency_data_record, mock_get_session):
        """Test if insert_currency_data handles exceptions correctly."""
        mock_session = MagicMock()
        mock_get_session.return_value = MagicMock(return_value=mock_session)

        # Mock data
        data = [
            {'time': '2023-05-01T15:45:30.123456Z', 'mid': {'o': '1.1000', 'h': '1.2000', 'l': '1.0500', 'c': '1.1500'},
             'volume': 1000}
        ]
        currency_data_mock = MagicMock()
        mock_create_currency_data_record.return_value = currency_data_mock

        # Ensure record_exists always returns False to simulate new records
        mock_record_exists.return_value = False

        # Add logging to debug
        logging.debug("Setting side effect for bulk_save_objects")
        mock_session.bulk_save_objects.side_effect = SQLAlchemyError("Insertion error")

        logging.debug("Calling insert_currency_data")
        try:
            with self.assertRaises(SQLAlchemyError):
                insert_currency_data(data)
            logging.debug("Assertion for SQLAlchemyError passed")
        except Exception as e:
            logging.error(f"Error: {e}")
            raise

        mock_session.rollback.assert_called_once()
        mock_session.close.assert_called_once()

if __name__ == "__main__":
    unittest.main()
