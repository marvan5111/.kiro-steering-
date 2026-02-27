import subprocess
import json

# Run nova_script.py
print("Running Nova script...")
subprocess.run(["python", "nova_script.py"])

# Show the last entry in audit_ledger.json
with open("audit_ledger.json", "r") as f:
    ledger = json.load(f)

last_entry = ledger[-1]
print("\nLast audit ledger entry:")
print(json.dumps(last_entry, indent=2))
