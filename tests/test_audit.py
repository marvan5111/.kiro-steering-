import unittest
import os
import json
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from audit.audit import AuditLogger

class TestAuditLogger(unittest.TestCase):

    def setUp(self):
        self.test_file = 'test_audit_ledger.json'
        self.audit = AuditLogger(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_log_decision(self):
        hash_val = self.audit.log_decision("12345", "Route A", "approved", {"score": 95})
        self.assertIsInstance(hash_val, str)
        self.assertEqual(len(hash_val), 64)  # SHA256 hex length
        self.assertEqual(len(self.audit.ledger), 1)

    def test_get_logs_all(self):
        self.audit.log_decision("12345", "Route A", "approved")
        self.audit.log_decision("67890", "Route B", "rejected")
        logs = self.audit.get_logs()
        self.assertEqual(len(logs), 2)

    def test_get_logs_filtered(self):
        self.audit.log_decision("12345", "Route A", "approved")
        self.audit.log_decision("67890", "Route B", "rejected")
        logs = self.audit.get_logs("12345")
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]['data']['shipment_id'], "12345")

    def test_verify_integrity_valid(self):
        self.audit.log_decision("12345", "Route A", "approved")
        self.assertTrue(self.audit.verify_integrity())

    def test_verify_integrity_invalid_hash(self):
        self.audit.log_decision("12345", "Route A", "approved")
        # Tamper with hash
        self.audit.ledger[0]['hash'] = 'tampered'
        self.assertFalse(self.audit.verify_integrity())

    def test_verify_integrity_broken_chain(self):
        self.audit.log_decision("12345", "Route A", "approved")
        self.audit.log_decision("67890", "Route B", "rejected")
        # Tamper with previous_hash
        self.audit.ledger[1]['data']['previous_hash'] = 'tampered'
        self.assertFalse(self.audit.verify_integrity())

if __name__ == '__main__':
    unittest.main()
