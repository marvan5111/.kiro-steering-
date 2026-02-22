import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from automation.automation import UIAutomation

class TestUIAutomation(unittest.TestCase):

    @patch('automation.automation.webdriver.Chrome')
    def setUp(self, mock_driver):
        self.mock_driver = MagicMock()
        mock_driver.return_value = self.mock_driver
        self.automation = UIAutomation()

    def test_login_to_portal_success(self):
        self.mock_driver.find_element.return_value = MagicMock()
        self.mock_driver.get = MagicMock()
        # Mock WebDriverWait
        with patch('automation.automation.WebDriverWait') as mock_wait:
            mock_wait.return_value.until = MagicMock()
            result = self.automation.login_to_portal("http://example.com", "user", "pass")
            self.assertTrue(result)

    def test_scrape_shipment_status_success(self):
        mock_element = MagicMock()
        mock_element.text = "In Transit"
        self.mock_driver.find_element.return_value = mock_element
        with patch('automation.automation.WebDriverWait') as mock_wait:
            mock_wait.return_value.until = MagicMock()
            result = self.automation.scrape_shipment_status("12345")
            self.assertEqual(result, "In Transit")

    def test_rebook_shipment_success(self):
        self.mock_driver.find_element.return_value = MagicMock()
        with patch('automation.automation.WebDriverWait') as mock_wait:
            mock_wait.return_value.until = MagicMock()
            result = self.automation.rebook_shipment("12345", "New Route")
            self.assertTrue(result)

    @patch('automation.automation.time.sleep')
    def test_retry_on_failure(self, mock_sleep):
        self.mock_driver.find_element.side_effect = Exception("Element not found")
        with self.assertRaises(Exception):
            self.automation.login_to_portal("http://example.com", "user", "pass")
        # Should have retried max_retries times
        self.assertEqual(self.mock_driver.find_element.call_count, 3)

if __name__ == '__main__':
    unittest.main()
