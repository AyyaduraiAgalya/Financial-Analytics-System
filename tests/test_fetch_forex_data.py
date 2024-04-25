import pandas as pd
import numpy as np
import unittest
import requests_mock
from scripts.fetch_forex_data import fetch_forex_data, clean_data

class TestFetchForexData(unittest.TestCase):

    @requests_mock.Mocker()
    def test_fetch_data_success(self, mock_get):
        # Mocking the API response
        url = "https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles"
        mock_response = {
            "candles": [
                {"time": "2020-01-01T00:00:00Z", "mid": {"c": "1.12345"}},
                {"time": "2020-01-02T00:00:00Z", "mid": {"c": "1.23456"}}
            ]
        }
        mock_get.get(url, json=mock_response, status_code=200)

        # Call the function
        df = fetch_forex_data("fake_api_key")

        # Assertions to check if the function works as expected
        self.assertEqual(len(df), 2)
        self.assertAlmostEqual(float(df.loc['2020-01-01', 'close']), 1.12345)

    @requests_mock.Mocker()
    def test_fetch_data_failure(self, mock_get):
        # Simulating a failure
        url = "https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles"
        mock_get.get(url, status_code=400)

        # Call the function
        df = fetch_forex_data("fake_api_key")
        self.assertIsNone(df)

    def test_clean_data(self):
        # Create test data with potential NA values and incorrect date formats
        test_data = pd.DataFrame({
            'time': ['2020-01-01', '2020-01-01', '2020-01-02', '2020-01-03', None, '2020-01-05'],
            'close': ['1.12345', '1.12345', '1.23456', np.nan, '1.34567', '1.45678']
        })
        test_data['time'] = pd.to_datetime(test_data['time'], errors='coerce')

        # Calling the clean_data function
        cleaned_data = clean_data(test_data)

        # Check that NA values are handled correctly
        self.assertFalse(cleaned_data.isna().any(axis=None))

        # Check that no duplicates remain
        self.assertEqual(cleaned_data.shape[0], 3)  # Assuming clean_data also drops NA rows

# If running pytest, use this
if __name__ == '__main__':
    unittest.main()
