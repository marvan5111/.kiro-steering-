import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from notifications.notifications import NotificationManager, slack_interactive, app

class TestNotificationManager(unittest.TestCase):
    def setUp(self):
        self.manager = NotificationManager(slack_webhook_url="https://hooks.slack.com/test")

    @patch('notifications.notifications.requests.post')
    def test_send_rerouting_proposal_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        proposals = [
            {"route": "Route A", "cost": 1.1, "time": 1.05, "compliance": 0.9, "score": 1.2}
        ]
        self.manager.send_rerouting_proposal("123", proposals)

        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], "https://hooks.slack.com/test")
        self.assertIn("blocks", kwargs["json"])

    @patch('notifications.notifications.requests.post')
    def test_send_rerouting_proposal_failure(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_post.return_value = mock_response

        proposals = [{"route": "Route A", "cost": 1.1, "time": 1.05, "compliance": 0.9, "score": 1.2}]
        with patch('notifications.notifications.logger') as mock_logger:
            self.manager.send_rerouting_proposal("123", proposals)
            mock_logger.error.assert_called()

    def test_send_rerouting_proposal_no_webhook(self):
        manager = NotificationManager()
        proposals = [{"route": "Route A", "cost": 1.1, "time": 1.05, "compliance": 0.9, "score": 1.2}]
        with patch('notifications.notifications.logger') as mock_logger:
            manager.send_rerouting_proposal("123", proposals)
            mock_logger.warning.assert_called_with("Slack webhook URL not set, skipping notification")

    @patch('notifications.notifications.AuditLogger')
    def test_handle_approval_approve(self, mock_audit_class):
        mock_audit = MagicMock()
        mock_audit_class.return_value = mock_audit

        manager = NotificationManager()
        payload = '{"shipment_id": "123", "route": "Route A", "action": "approve"}'
        manager.handle_approval(payload)

        mock_audit.log_decision.assert_called_with("123", "Route A", "approved", {"source": "slack"})

    @patch('notifications.notifications.AuditLogger')
    def test_handle_approval_reject(self, mock_audit_class):
        mock_audit = MagicMock()
        mock_audit_class.return_value = mock_audit

        manager = NotificationManager()
        payload = '{"shipment_id": "123", "action": "reject"}'
        manager.handle_approval(payload)

        mock_audit.log_decision.assert_called_with("123", "none", "rejected", {"source": "slack"})

    @patch('notifications.notifications.NotificationManager')
    def test_slack_interactive_callback(self, mock_manager_class):
        mock_manager = MagicMock()
        mock_manager_class.return_value = mock_manager

        with patch('notifications.notifications.notification_manager', mock_manager):
            with app.test_client() as client:
                payload = '{"actions": [{"value": "{\\"shipment_id\\": \\"123\\", \\"action\\": \\"approve\\"}"}]}'
                response = client.post('/slack/interactive', data={'payload': payload})

        self.assertEqual(response.status_code, 200)
        mock_manager.handle_approval.assert_called_with('{"shipment_id": "123", "action": "approve"}')

if __name__ == '__main__':
    unittest.main()
