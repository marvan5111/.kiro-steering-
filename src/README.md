# Source Code Structure

This `src/` folder contains the implementation of the shipment steering system components.

## Folder Structure

- `ingestion/`: Data ingestion layer for fetching shipment data and external signals.
- `reasoning/`: AI reasoning engine for evaluating risks and proposing rerouting options.
- `automation/`: UI automation scripts for handling legacy systems without APIs.
- `audit/`: Blockchain audit layer for immutable logging of decisions.
- `notifications/`: Notification layer for sending alerts and approvals.
- `dashboard/`: Frontend dashboard for auditors and users.

## Architecture Diagram

```
[External Signals: Weather API, Strike News]
          |
          v
[Ingestion Layer] --> [Reasoning Engine] --> [Proposals]
          |                    |
          v                    v
[Audit Ledger]       [Notifications (Slack)]
          ^
          |
[Interactive Callbacks] --> [Approval/Rejection]
```

## How to Run Locally

1. Install dependencies: `pip install flask requests` (or from requirements.md).
2. Configure environment variables (see Configuration below).
3. Run the reasoning engine: `python src/reasoning/engine.py`
4. To handle Slack callbacks: `python -c "from src.notifications.notifications import NotificationManager; n = NotificationManager(); n.start_server(port=3000)"`

## Configuration

- `SLACK_WEBHOOK_URL`: Set this environment variable to your Slack webhook URL (obtained from Slack App > Incoming Webhooks). Example: `export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/SERVICE/ID"`

## Example Outputs

### Risk Evaluation
```
INFO: High weather risk detected
INFO: High strike risk detected
INFO: Overall risk score: 1.0
```

### Rerouting Proposals
```
INFO: Generated 3 rerouting proposals
Proposals:
- Alternative Route B: Cost 1.2, Time 0.95, Compliance 1.0, Score 1.06
- Alternative Route A: Cost 1.1, Time 1.05, Compliance 0.9, Score 1.08
- Alternative Route C: Cost 0.9, Time 1.2, Compliance 0.8, Score 1.09
```

### Slack Notification
When `SLACK_WEBHOOK_URL` is set, proposals are posted to Slack with interactive buttons for approval/rejection. Example message:

"Rerouting Proposal for Shipment 12345

Disruption detected. Please review and approve the best rerouting option.

• Alternative Route B: Cost 1.20, Time 0.95, Compliance 1.00, Score 1.06
• Alternative Route A: Cost 1.10, Time 1.05, Compliance 0.90, Score 1.08
• Alternative Route C: Cost 0.90, Time 1.20, Compliance 0.80, Score 1.09

[Approve Alternative Route B] [Reject]"

Approvals/rejections are handled via callbacks and logged in the audit ledger.
