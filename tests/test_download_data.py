import unittest
from unittest.mock import patch
import os
import requests
from src.data_gathering.download_data import check_connection


class TestDownloadData(unittest.TestCase):

    # Test for check_connection function
    @patch('requests.get')
    def test_check_connection(self, mock_get):
        # Successful connection
        mock_get.return_value.status_code = 200
        self.assertDictEqual({True: ""}, check_connection())

        # HTTP error
        mock_get.return_value.raise_for_status = requests.exceptions.HTTPError("404 Client Error: Not Found for url")
        self.assertDictEqual({False: "HTTP error occurred: 404 Client Error: Not Found for url"}, check_connection())

        # Timeout exception
        mock_get.side_effect = requests.Timeout
        self.assertDictEqual({False: "Timeout error occurred: "}, check_connection())

        # Request exception
        mock_get.side_effect = requests.exceptions.RequestException("Request error")
        self.assertDictEqual({False: "Request error occurred: Request error"}, check_connection())

    @patch('requests.get')
    def test_download_turtles_info(self, mock_get):
        # Successful download


if __name__ == '__main__':
    unittest.main()
