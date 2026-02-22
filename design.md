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
## Requirements-to-Design Mapping

### Reliability
- Requirement: When shipment data is updated, the system shall automatically check for risks.
  - Design: Implemented by the **Data Ingestion Layer** + **Reasoning Engine**.
- Requirement: When external signals (e.g., weather alerts, strike news) are received, the system shall evaluate their impact on shipments.
  - Design: **MCP connectors** feed external signals into the **Reasoning Engine**.
- Requirement: The system shall continuously monitor shipment feeds to detect disruptions.
  - Design: **Monitoring Agent** runs on a schedule via CloudWatch/Lambda.

### Automation
- Requirement: When a disruption is detected, the system shall propose rerouting options balancing cost, time, and compliance.
  - Design: **Reasoning Engine** generates rerouting proposals with trade-offs.
- Requirement: Where a carrier does not provide an API, the system shall use UI automation to log in, scrape shipment status, and rebook shipments.
  - Design: **UI Automation Layer** (Nova Act or Selenium).
- Requirement: When rerouting is required, the system shall notify humans via Slack for approval.
  - Design: **Notification Layer** integrates with Slack API.

### Auditability
- Requirement: The system shall record every rerouting decision on a blockchain ledger.
  - Design: **Blockchain Audit Layer** (Amazon Managed Blockchain).
- Requirement: The system shall store reasoning traces, shipment IDs, and approval status immutably.
  - Design: **Audit Database** + **Blockchain Ledger**.
- Requirement: The system shall provide an auditor-friendly dashboard to review past decisions.
  - Design: **Dashboard UI** built with AWS Amplify or React frontend.
