import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ingestion.ingest import fetch_shipment_data, fetch_weather_alerts, fetch_strike_news, main

class TestIngestion(unittest.TestCase):

    @patch('ingestion.ingest.requests.get')
    def test_fetch_shipment_data_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"shipment": "data"}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = fetch_shipment_data("http://example.com")
        self.assertEqual(result, {"shipment": "data"})
        mock_get.assert_called_once_with("http://example.com", timeout=10)

    @patch('ingestion.ingest.requests.get')
    def test_fetch_shipment_data_failure(self, mock_get):
        import requests
        mock_get.side_effect = requests.RequestException("Network error")

        result = fetch_shipment_data("http://example.com")
        self.assertIsNone(result)

    @patch('ingestion.ingest.requests.get')
    def test_fetch_weather_alerts_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"weather": "alerts"}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = fetch_weather_alerts("http://weather.com")
        self.assertEqual(result, {"weather": "alerts"})

    @patch('ingestion.ingest.requests.get')
    def test_fetch_strike_news_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"strike": "news"}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = fetch_strike_news("http://news.com")
        self.assertEqual(result, {"strike": "news"})

if __name__ == '__main__':
    unittest.main()
