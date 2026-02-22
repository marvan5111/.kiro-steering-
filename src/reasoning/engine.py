import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReasoningEngine:
    def __init__(self, cost_weight=0.4, time_weight=0.4, compliance_weight=0.2):
        self.cost_weight = cost_weight
        self.time_weight = time_weight
        self.compliance_weight = compliance_weight

    def evaluate_risk(self, shipment_data, weather_data, strike_data):
        """
        Evaluate risk based on external signals.
        Returns a risk score (0-1, higher means higher risk).
        """
        risk_score = 0.0

        if weather_data and any(alert.get('severity', 0) > 5 for alert in weather_data.get('alerts', [])):
            risk_score += 0.3
            logger.info("High weather risk detected")

        if strike_data and any(strike.get('impact', 'low') == 'high' for strike in strike_data.get('strikes', [])):
            risk_score += 0.4
            logger.info("High strike risk detected")

        # Add shipment-specific checks, e.g., if shipment is in risky area
        if shipment_data and shipment_data.get('location') in ['risky_area1', 'risky_area2']:
            risk_score += 0.3

        risk_score = min(risk_score, 1.0)
        logger.info(f"Overall risk score: {risk_score}")
        return risk_score

    def generate_rerouting_proposals(self, current_route, risk_score):
        """
        Generate rerouting options if risk > threshold.
        Each proposal has cost, time, compliance score.
        """
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
        return scored_proposals

def main():
    engine = ReasoningEngine()
    # Example data
    shipment = {"location": "risky_area1"}
    weather = {"alerts": [{"severity": 7}]}
    strike = {"strikes": [{"impact": "high"}]}

    risk = engine.evaluate_risk(shipment, weather, strike)
    proposals = engine.generate_rerouting_proposals("current_route", risk)
    return {"risk": risk, "proposals": proposals}

if __name__ == "__main__":
    result = main()
    print(result)
