# Tasks.md

## Data Ingestion Layer
- Implement connectors to ingest shipment feeds.
- Integrate weather alerts and strike news via APIs.
- Set up monitoring agent with AWS CloudWatch/Lambda.

## Reasoning Engine
- Build AI reasoning module using Amazon Nova 2 Lite.
- Define logic for evaluating rerouting options (cost, time, compliance).
- Implement trade-off analysis and decision scoring.

## UI Automation Layer
- Develop automation scripts with Nova Act or Selenium.
- Handle login workflows for legacy portals.
- Scrape shipment status and rebook shipments when APIs are unavailable.
- Add retry logic for failed automation attempts.

## Blockchain Audit Layer
- Configure Amazon Managed Blockchain.
- Record rerouting decisions immutably.
- Store reasoning traces, shipment IDs, and approval status.
- Build query interface for auditors.

## Notification Layer
- Integrate Slack API for human approval notifications.
- Format messages with shipment details and rerouting proposals.
- Log approval/rejection outcomes.

## Dashboard UI
- Build frontend with AWS Amplify or React.
- Display shipment status, rerouting history, and audit logs.
- Provide filters for auditors to review past decisions.
