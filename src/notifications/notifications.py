import logging
import requests
import json
import sys
import os
import boto3
from flask import Flask, request

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from audit.audit import AuditLogger

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
notification_manager = None

@app.route('/slack/interactive', methods=['POST'])
def slack_interactive():
    global notification_manager
    if not notification_manager:
        notification_manager = NotificationManager()

    payload_str = request.form.get('payload')
    if payload_str:
        payload = json.loads(payload_str)
        action = payload.get('actions', [{}])[0]
        value = action.get('value')
        if value:
            notification_manager.handle_approval(value)
    return '', 200

class NotificationManager:
    def __init__(self, slack_webhook_url=None):
        self.slack_webhook_url = slack_webhook_url or os.getenv('SLACK_WEBHOOK_URL')
        self.audit = AuditLogger()
        self.nova = boto3.client("bedrock-runtime")

    def call_nova(self, prompt):
        """
        Call Amazon Nova for generating summaries.
        """
        try:
            response = self.nova.invoke_model(
                modelId="amazon.nova-pro",
                body=json.dumps({
                    "inputText": prompt,
                    "parameters": {"temperature": 0.7, "maxTokens": 300}
                })
            )
            result = json.loads(response['body'].read())
            return {
                'outputText': result.get('outputText', ''),
                'stopReason': result.get('stopReason'),
                'usage': result.get('usage', {}),
                'modelId': "amazon.nova-pro",
                'region': self.nova.meta.region_name
            }
        except Exception as e:
            logger.error(f"Nova call failed: {e}")
            return None

    def send_rerouting_proposal(self, shipment_id, proposals, explanation=""):
        """
        Send rerouting proposal to Slack with approval buttons.
        """
        if not self.slack_webhook_url:
            logger.warning("Slack webhook URL not set, skipping notification")
            return

        # Use Nova to generate human-friendly summary
        prompt = f"Summarize the rerouting proposals for shipment {shipment_id}. Risk explanation: {explanation}. Proposals: {proposals}. Provide a concise, human-friendly message for Slack."
        nova_summary = self.call_nova(prompt)
        if nova_summary:
            proposal_text = nova_summary['outputText']
        else:
            # Fallback to raw list
            proposal_text = "\n".join([f"• {p['route']}: Cost {p['cost']:.2f}, Time {p['time']:.2f}, Compliance {p['compliance']:.2f}, Score {p['score']:.2f}" for p in proposals])

        # Format message with shipment details and proposals
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Rerouting Proposal for Shipment {shipment_id}*\n\n{explanation}\n\nPlease review and approve the best rerouting option."
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": proposal_text
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": f"Approve {proposals[0]['route']}"
                        },
                        "value": json.dumps({"shipment_id": shipment_id, "route": proposals[0]['route'], "action": "approve"}),
                        "action_id": "approve_rerouting"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Reject"
                        },
                        "value": json.dumps({"shipment_id": shipment_id, "action": "reject"}),
                        "action_id": "reject_rerouting"
                    }
                ]
            }
        ]

        payload = {
            "blocks": blocks
        }

        try:
            response = requests.post(self.slack_webhook_url, json=payload, timeout=10)
            if response.status_code == 200:
                logger.info(f"Sent rerouting proposal for shipment {shipment_id} to Slack")
            else:
                logger.error(f"Failed to send Slack message: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"Error sending Slack notification: {e}")

    def send_message(self, text):
        """
        Send a simple text message to Slack.
        """
        if not self.slack_webhook_url:
            logger.warning("Slack webhook URL not set, skipping notification")
            return

        payload = {"text": text}

        try:
            response = requests.post(self.slack_webhook_url, json=payload, timeout=10)
            if response.status_code == 200:
                logger.info("Sent message to Slack")
            else:
                logger.error(f"Failed to send Slack message: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"Error sending Slack notification: {e}")

    def handle_approval(self, payload):
        """
        Handle approval/rejection from Slack interaction.
        Payload is the value from the button.
        """
        data = json.loads(payload)
        shipment_id = data['shipment_id']
        action = data['action']

        if action == 'approve':
            route = data['route']
            logger.info(f"Approved rerouting for shipment {shipment_id} to {route}")
            # Log approval in audit
            self.audit.log_decision(shipment_id, route, "approved", {"source": "slack"})
        elif action == 'reject':
            logger.info(f"Rejected rerouting for shipment {shipment_id}")
            # Log rejection
            self.audit.log_decision(shipment_id, "none", "rejected", {"source": "slack"})

    def start_server(self, port=3000):
        """
        Start the Flask server to handle Slack interactive callbacks.
        """
        global notification_manager
        notification_manager = self
        logger.info(f"Starting Slack callback server on port {port}")
        app.run(port=port)

def main():
    # Example usage
    manager = NotificationManager()
    proposals = [
        {"route": "Alternative Route A", "cost": 1.1, "time": 1.05, "compliance": 0.9, "score": 1.2},
        {"route": "Alternative Route B", "cost": 1.2, "time": 0.95, "compliance": 1.0, "score": 1.1}
    ]
    manager.send_rerouting_proposal("12345", proposals)

if __name__ == "__main__":
    main()
