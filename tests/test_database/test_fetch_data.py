import unittest
from unittest.mock import patch
from scripts.fetch_data import fetch_data

class TestFetchData(unittest.TestCase):

    @patch('database.fetch_data.requests.get')
    def test_fetch_data(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "candles": [
                {'complete': True, 'volume': 79964, 'time': '2023-12-28T22:00:00.000000Z', 'mid': {'o': '1.10630', 'h': '1.10844', 'l': '1.10342', 'c': '1.10374'}},
                {'complete': True, 'volume': 86969, 'time': '2024-01-01T22:00:00.000000Z', 'mid': {'o': '1.10440', 'h': '1.10453', 'l': '1.09383', 'c': '1.09406'}}
            ]
        }

        data = fetch_data()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['time'], '2023-12-28T22:00:00.000000Z')
        self.assertEqual(data[0]['mid']['o'], '1.10630')

if __name__ == '__main__':
    unittest.main()
