# Design.md

## System Overview
The Dynamic Supply Chain Resilience Bot is a self-healing logistics system that monitors shipment data and external signals, detects disruptions, and autonomously reroutes shipments. It integrates AI reasoning, UI automation, and blockchain audit trails.

## Components
- **Data Ingestion Layer**: Collects shipment feeds, weather alerts, and strike news.
- **Reasoning Engine**: Evaluates rerouting options balancing cost, time, and compliance.
- **UI Automation Layer**: Logs into legacy portals, scrapes shipment status, and rebooks shipments when APIs are unavailable.
- **Blockchain Audit Layer**: Records decisions immutably for compliance and transparency.
- **Notification Layer**: Sends alerts to humans via Slack for approvals.

## Data Flow
1. Shipment data and external signals are ingested.
2. Reasoning engine evaluates risks and rerouting options.
3. If API is unavailable, UI automation executes portal workflows.
4. Decision is recorded on blockchain.
5. Slack notification is sent for human approval.

## Integration Points
- AI reasoning engine (Nova 2 Lite or chosen model).
- UI automation (Nova Act, Selenium, or RPA tools).
- Blockchain (Amazon Managed Blockchain).
- Slack API for notifications.

## Reliability & Error Handling
- Continuous monitoring of shipment feeds.
- Retry logic for failed portal logins.
- Fallback rerouting strategies if automation fails.
