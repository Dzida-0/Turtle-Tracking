import unittest
from unittest.mock import patch
import os
import requests
from src.data_gathering.download_data import check_connection


class TestDownloadData(unittest.TestCase):

    # Test for check_connection function
    @patch('requests.get')
    def test_check_connection(self, mock_get):
        # Simulate a successful response
        mock_get.return_value.status_code = 200
        self.assertTrue(check_connection())

        # Simulate a failed response
        mock_get.return_value.status_code = 404
        self.assertFalse(check_connection())

        # Simulate an exception (e.g., Timeout)
        mock_get.side_effect = requests.Timeout
        self.assertFalse(check_connection())


if __name__ == '__main__':
    unittest.main()
