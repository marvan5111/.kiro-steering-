# Requirements.md (EARS Notation)

## Reliability
- When shipment data is updated, the system shall automatically check for risks.
- When external signals (e.g., weather alerts, strike news) are received, the system shall evaluate their impact on shipments.
- The system shall continuously monitor shipment feeds to detect disruptions.

## Automation
- When a disruption is detected, the system shall propose rerouting options balancing cost, time, and compliance.
- Where a carrier does not provide an API, the system shall use UI automation to log in, scrape shipment status, and rebook shipments.
- When rerouting is required, the system shall notify humans via Slack for approval.

## Auditability
- The system shall record every rerouting decision on a blockchain ledger.
- The system shall store reasoning traces, shipment IDs, and approval status immutably.
- The system shall provide an auditor-friendly dashboard to review past decisions.

## Dependencies
- Flask: For handling Slack interactive component callbacks.
- requests: For sending HTTP requests to Slack webhooks.
- boto3: For AWS Bedrock/Nova API calls.
- Other standard libraries: json, logging, os, sys.
