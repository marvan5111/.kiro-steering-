import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from reasoning.engine import ReasoningEngine

class TestReasoning(unittest.TestCase):

    def test_evaluate_risk_low(self):
        engine = ReasoningEngine()
        shipment = {"location": "safe_area"}
        weather = {"alerts": [{"severity": 3}]}
        strike = {"strikes": [{"impact": "low"}]}

        risk = engine.evaluate_risk(shipment, weather, strike)
        self.assertEqual(risk, 0.0)

    def test_evaluate_risk_high(self):
        engine = ReasoningEngine()
        shipment = {"location": "risky_area1"}
        weather = {"alerts": [{"severity": 7}]}
        strike = {"strikes": [{"impact": "high"}]}

        risk = engine.evaluate_risk(shipment, weather, strike)
        self.assertEqual(risk, 1.0)  # 0.3 + 0.4 + 0.3 = 1.0

    def test_generate_rerouting_proposals_low_risk(self):
        engine = ReasoningEngine()
        proposals = engine.generate_rerouting_proposals("current", 0.3)
        self.assertEqual(proposals, [])

    def test_generate_rerouting_proposals_high_risk(self):
        engine = ReasoningEngine()
        proposals = engine.generate_rerouting_proposals("current", 0.7)
        self.assertEqual(len(proposals), 3)
        # Check sorted by score
        self.assertLessEqual(proposals[0]['score'], proposals[1]['score'])

    def test_custom_weights(self):
        engine = ReasoningEngine(cost_weight=0.5, time_weight=0.3, compliance_weight=0.2)
        self.assertEqual(engine.cost_weight, 0.5)
        self.assertEqual(engine.time_weight, 0.3)
        self.assertEqual(engine.compliance_weight, 0.2)

if __name__ == '__main__':
    unittest.main()
