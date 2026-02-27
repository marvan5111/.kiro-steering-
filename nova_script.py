import boto3
import json
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.audit.audit import AuditLogger
from src.notifications.notifications import NotificationManager

def main():
    # Initialize clients
    nova_client = boto3.client("bedrock-runtime")
    audit = AuditLogger()
    notifications = NotificationManager()

    # Example prompt
    prompt = "Explain the importance of AI in supply chain management."

    try:
        # Call Nova
        response = nova_client.invoke_model(
            modelId="amazon.nova-pro",
            body=json.dumps({
                "inputText": prompt,
                "parameters": {"temperature": 0.7, "maxTokens": 300}
            })
        )
        result = json.loads(response['body'].read())
        output = result.get('outputText', 'No response')

        # Print response
        print("Nova Response:")
        print(output)

        # Log to audit ledger
        audit.log_decision("nova_demo", "response_generated", "completed", {"prompt": prompt, "response": output})

        # Send to Slack
        notifications.send_message(f"Nova Response: {output}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
