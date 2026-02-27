import logging
import sys
import os
import boto3
import json

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from audit.audit import AuditLogger
from notifications.notifications import NotificationManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReasoningEngine:
    def __init__(self, cost_weight=0.4, time_weight=0.4, compliance_weight=0.2):
        self.cost_weight = cost_weight
        self.time_weight = time_weight
        self.compliance_weight = compliance_weight
        self.audit = AuditLogger()
        self.nova = boto3.client("bedrock-runtime")

    def call_nova(self, prompt):
        """
        Call Amazon Nova for AI predictions.
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

    def evaluate_risk(self, shipment_data, weather_data, strike_data):
        """
        Evaluate risk based on external signals using Nova for predictive scoring.
        Returns a dict with 'score' (0-1, higher means higher risk) and 'explanation'.
        """
        # Fallback manual calculation
        risk_score = 0.0
        explanation = ""

        if weather_data and any(alert.get('severity', 0) > 5 for alert in weather_data.get('alerts', [])):
            risk_score += 0.3
            explanation += "High weather risk detected. "

        if strike_data and any(strike.get('impact', 'low') == 'high' for strike in strike_data.get('strikes', [])):
            risk_score += 0.4
            explanation += "High strike risk detected. "

        if shipment_data and shipment_data.get('location') in ['risky_area1', 'risky_area2']:
            risk_score += 0.3
            explanation += "Shipment in risky area. "

        risk_score = min(risk_score, 1.0)

        # Use Nova for predictive risk
        prompt = f"Evaluate the risk for shipment at location {shipment_data.get('location', 'unknown')} with weather alerts {weather_data} and strike data {strike_data}. Provide a risk score from 0 to 1 and a brief explanation."
        nova_response = self.call_nova(prompt)
        if nova_response:
            # Parse Nova response, assume format "Risk score: X. Explanation: Y."
            try:
                lines = nova_response['outputText'].split('. ')
                score_line = [l for l in lines if 'Risk score' in l]
                if score_line:
                    score_str = score_line[0].split(':')[1].strip()
                    risk_score = float(score_str)
                exp_line = [l for l in lines if 'Explanation' in l]
                if exp_line:
                    explanation = exp_line[0].split(':', 1)[1].strip()
            except:
                logger.warning("Failed to parse Nova response, using fallback")

        logger.info(f"Overall risk score: {risk_score}, Explanation: {explanation}")
        return {'score': risk_score, 'explanation': explanation}

    def generate_rerouting_proposals(self, shipment_id, current_route, risk_data):
        """
        Generate rerouting options if risk > threshold.
        risk_data is dict with 'score' and 'explanation'.
        """
        risk_score = risk_data['score']
        explanation = risk_data['explanation']
        if risk_score < 0.5:
            logger.info("No rerouting needed, risk is low")
            return []

        proposals = [
            {"route": "Alternative Route A", "cost": 1.1, "time": 1.05, "compliance": 0.9},
            {"route": "Alternative Route B", "cost": 1.2, "time": 0.95, "compliance": 1.0},
            {"route": "Alternative Route C", "cost": 0.9, "time": 1.2, "compliance": 0.8}
        ]

        scored_proposals = []
        for prop in proposals:
            score = (self.cost_weight * prop['cost'] +
                     self.time_weight * prop['time'] +
                     self.compliance_weight * (1 / prop['compliance']))  # Lower compliance increases score (penalty)
            prop['score'] = score
            scored_proposals.append(prop)

        # Sort by score (lower is better)
        scored_proposals.sort(key=lambda x: x['score'])
        logger.info(f"Generated {len(scored_proposals)} rerouting proposals")

        # Log proposals in audit ledger
        for prop in scored_proposals:
            self.audit.log_decision(shipment_id, prop['route'], "proposed", {"score": prop['score'], "cost": prop['cost'], "time": prop['time'], "compliance": prop['compliance'], "risk_explanation": explanation})

        # Send notification to Slack
        notifications = NotificationManager()
        notifications.send_rerouting_proposal(shipment_id, scored_proposals, explanation)

        return scored_proposals

def main():
    engine = ReasoningEngine()
    # Example data
    shipment = {"location": "risky_area1"}
    weather = {"alerts": [{"severity": 7}]}
    strike = {"strikes": [{"impact": "high"}]}

    risk = engine.evaluate_risk(shipment, weather, strike)
    proposals = engine.generate_rerouting_proposals("12345", "current_route", risk)
    return {"risk": risk, "proposals": proposals}

if __name__ == "__main__":
    result = main()
    print(result)
