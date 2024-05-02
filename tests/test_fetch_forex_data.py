import unittest
import numpy as np
import pandas as pd
import requests_mock
from scripts.fetch_forex_data import fetch_forex_data, clean_data

class TestFetchForexData(unittest.TestCase):
    """
    A suite of tests to validate the behavior of the forex data fetching and cleaning functions.
    """

    @requests_mock.Mocker()
    def test_fetch_data_success(self, mock_get):
        """
        Test successful API call to fetch forex data and checks the integrity of the returned DataFrame.
        """
        # Setup the URL and mock response for the test
        url = "https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles"
        mock_response = {
            "candles": [
                {"time": "2020-01-01T00:00:00Z", "mid": {"c": "1.12345"}},
                {"time": "2020-01-02T00:00:00Z", "mid": {"c": "1.23456"}}
            ]
        }
        # Mock the GET request to return predefined data
        mock_get.get(url, json=mock_response, status_code=200)

        # Call the function under test
        df = fetch_forex_data("fake_api_key")

        # Assert that the DataFrame contains the correct number of entries and values match expected results
        self.assertEqual(len(df), 2)
        np.testing.assert_array_almost_equal(df['close'].values, [1.12345, 1.23456])

    @requests_mock.Mocker()
    def test_fetch_data_failure(self, mock_get):
        """
        Test the response handling when the API call fails (e.g., HTTP 400 error).
        """
        # Define the API endpoint and simulate a 400 Bad Request error
        url = "https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles"
        mock_get.get(url, status_code=400)

        # Call the function and expect it to handle the error gracefully
        df = fetch_forex_data("fake_api_key")

        # Verify that the function returns None when an API error occurs
        self.assertIsNone(df)

    def test_clean_data(self):
        """
        Test the cleaning of forex data to handle potential anomalies like duplicate records and NaN values.
        """
        # Sample data simulating fetched forex prices
        test_data = pd.DataFrame({
            'time': ['2020-01-01', '2020-01-01', '2020-01-02', '2020-01-03', None, '2020-01-05'],
            'close': ['1.12345', '1.12345', '1.23456', np.nan, '1.34567', '1.45678']
        })
        # Convert time strings to datetime objects, handling errors
        test_data['time'] = pd.to_datetime(test_data['time'], errors='coerce')

        # Clean the data using the dedicated function
        cleaned_data = clean_data(test_data)

        # Ensure that after cleaning, no duplicate or NaN values exist, and the data count is correct
        self.assertFalse(cleaned_data.isna().any(axis=None))
        self.assertEqual(cleaned_data.shape[0], 3)  # Three unique dates should remain

    @requests_mock.Mocker()
    def test_integration_fetch_and_clean(self, mock_get):
        """
        Test the integration of data fetching and cleaning to ensure they work seamlessly together.
        """
        url = "https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles"
        mock_response = {
            "candles": [
                {"time": "2020-01-01T00:00:00Z", "mid": {"c": "1.12345"}},
                {"time": "2020-01-02T00:00:00Z", "mid": {"c": "1.23456"}},
                {"time": "2020-01-03T00:00:00Z", "mid": {"c": "not_a_number"}}
            ]
        }
        # Setup mock response with a data anomaly
        mock_get.get(url, json=mock_response, status_code=200)

        # Fetch and clean the data
        raw_data = fetch_forex_data("fake_api_key")
        cleaned_data = clean_data(raw_data)

        # Check the cleaned data for correctness
        self.assertEqual(len(cleaned_data), 2)
        self.assertFalse(cleaned_data.isna().any(axis=None))
        self.assertTrue(all(pd.to_numeric(cleaned_data['close'], errors='coerce').notna()))

# Run the tests if this file is executed directly
if __name__ == '__main__':
    unittest.main()

