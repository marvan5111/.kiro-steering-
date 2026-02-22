# Tasks.md

## Requirements-to-Design-to-Tasks Mapping

### Reliability
- Requirement: When shipment data is updated, the system shall automatically check for risks.
  - Design: Data Ingestion Layer + Reasoning Engine
  - Tasks:
    - Implement connectors for shipment feeds
    - Build risk evaluation logic in reasoning engine
    - Set up monitoring agent with CloudWatch/Lambda

- Requirement: When external signals are received, the system shall evaluate their impact.
  - Design: MCP connectors + Reasoning Engine
  - Tasks:
    - Integrate weather API
    - Integrate strike/news API
    - Feed signals into reasoning engine

### Automation
- Requirement: When a disruption is detected, the system shall propose rerouting options.
  - Design: Reasoning Engine
  - Tasks:
    - Define rerouting logic (cost, time, compliance)
    - Implement trade-off scoring
    - Generate rerouting proposals

- Requirement: Where no API exists, the system shall use UI automation.
  - Design: UI Automation Layer
  - Tasks:
    - Build Selenium/Nova Act scripts
    - Handle login workflows
    - Scrape shipment status
    - Automate rebooking

### Auditability
- Requirement: The system shall record every rerouting decision on blockchain.
  - Design: Blockchain Audit Layer
  - Tasks:
    - Configure Amazon Managed Blockchain
    - Write decision logs immutably
    - Store reasoning traces and shipment IDs

- Requirement: The system shall provide an auditor-friendly dashboard.
  - Design: Dashboard UI
  - Tasks:
    - Build React/AWS Amplify frontend
    - Display shipment history and audit logs
    - Add filters for auditors
