import hashlib
import json
import logging
import boto3
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuditLogger:
    def __init__(self, storage_file='audit_ledger.json'):
        self.storage_file = storage_file
        self.ledger = []
        self.load_ledger()
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

    def load_ledger(self):
        try:
            with open(self.storage_file, 'r') as f:
                self.ledger = json.load(f)
        except FileNotFoundError:
            self.ledger = []
            logger.info("Audit ledger initialized")

    def save_ledger(self):
        with open(self.storage_file, 'w') as f:
            json.dump(self.ledger, f, indent=4)

    def _compute_hash(self, data):
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

    def log_decision(self, shipment_id, rerouting_option, approval_status, reasoning_trace=None):
        """
        Log a rerouting decision immutably.
        """
        previous_hash = self.ledger[-1]['hash'] if self.ledger else '0' * 64
        timestamp = datetime.now(timezone.utc).isoformat()
        data = {
            'shipment_id': shipment_id,
            'rerouting_option': rerouting_option,
            'approval_status': approval_status,
            'reasoning_trace': reasoning_trace,
            'timestamp': timestamp,
            'previous_hash': previous_hash
        }
        # Generate Nova-powered compliance summary
        prompt = f"Generate a compliance-ready summary for this audit log entry: {data}"
        compliance_summary = self.call_nova(prompt)
        if compliance_summary:
            data['compliance_summary'] = compliance_summary['outputText']
            data['modelId'] = compliance_summary['modelId']
            data['region'] = compliance_summary['region']
            data['stopReason'] = compliance_summary['stopReason']
            data['usage'] = compliance_summary['usage']
        else:
            data['compliance_summary'] = "Summary not available"
        current_hash = self._compute_hash(data)
        entry = {
            'data': data,
            'hash': current_hash
        }
        self.ledger.append(entry)
        self.save_ledger()
        logger.info(f"Logged decision for shipment {shipment_id}: {approval_status}")
        return current_hash

    def get_logs(self, shipment_id=None):
        """
        Retrieve logs, optionally filtered by shipment_id.
        """
        if shipment_id:
            return [entry for entry in self.ledger if entry['data']['shipment_id'] == shipment_id]
        return self.ledger

    def verify_integrity(self):
        """
        Verify the immutability of the ledger by checking hash chain.
        """
        for i, entry in enumerate(self.ledger):
            expected_hash = self._compute_hash(entry['data'])
            if entry['hash'] != expected_hash:
                logger.error(f"Integrity check failed at entry {i}")
                return False
            if i > 0 and entry['data']['previous_hash'] != self.ledger[i-1]['hash']:
                logger.error(f"Chain broken at entry {i}")
                return False
        logger.info("Ledger integrity verified")
        return True

def main():
    audit = AuditLogger()
    # Example usage
    audit.log_decision("12345", "New Route A", "approved", {"cost": 100, "time": 2})
    logs = audit.get_logs("12345")
    print("Logs:", logs)
    print("Integrity:", audit.verify_integrity())

if __name__ == "__main__":
    main()
