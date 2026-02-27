import boto3
import json
from datetime import datetime

# Use your SSO profile
session = boto3.Session(profile_name="slalom_IsbUsersPS-176766376972")
client = session.client("bedrock-runtime", region_name="us-east-1")

# Read the prompt from input.json
with open("input.json", "r") as f:
    body = json.load(f)

prompt = body["messages"][0]["content"][0]["text"]

response = client.invoke_model(
    modelId="amazon.nova-lite-v1:0",
    body=json.dumps(body)
)

# Decode Nova's response
decoded = response["body"].read().decode("utf-8")
response_body = json.loads(decoded)

# Save to output.json
with open("output.json", "w") as f:
    json.dump(response_body, f, indent=2)

# Print the response
print("Nova Response:", decoded)

# Load existing audit ledger
ledger_path = "audit_ledger.json"
try:
    with open(ledger_path, "r") as f:
        ledger = json.load(f)
except FileNotFoundError:
    ledger = []

# Append new entry with expanded metadata
ledger.append({
    "timestamp": datetime.utcnow().isoformat(),
    "prompt": prompt,
    "response": decoded,
    "modelId": "amazon.nova-lite-v1:0",
    "region": "us-east-1",
    "stopReason": response_body.get("stopReason"),
    "usage": response_body.get("usage")
})

# Save back to audit ledger
with open(ledger_path, "w") as f:
    json.dump(ledger, f, indent=2)
