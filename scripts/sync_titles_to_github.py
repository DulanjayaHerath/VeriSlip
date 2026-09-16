#!/usr/bin/env python3
"""
Sync updated issue titles and labels to GitHub.
"""

import os
import json
import subprocess
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ISSUES_FILE = os.path.join(SCRIPT_DIR, "issues_data.json")

def main():
    repo = "chirana07/VeriSlip"
    with open(ISSUES_FILE, "r") as f:
        issues = json.load(f)

    # Ensure new domain labels exist
    new_labels = {
        "domain:cv-forensics": "1d76db",
        "domain:ml-data": "7057ff",
        "domain:backend-api": "0e8a16",
        "domain:infra-research": "5319e7",
        "contributions-welcome": "008672"
    }
    print("Ensuring open source labels exist...")
    for label, color in new_labels.items():
        cmd = ["gh", "label", "create", label, "--repo", repo, "--color", color, "--force"]
        subprocess.run(cmd, capture_output=True, text=True)

    print(f"Syncing titles and domain labels for {len(issues)} issues on {repo}...")
    # Issues 1 and 2 were already updated, sync 3 to 100
    for iss in issues:
        num = iss["number"]
        if num <= 2:
            continue
        cmd = [
            "gh", "issue", "edit", str(num),
            "--repo", repo,
            "--title", iss["title"]
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"  [✓] #{num}: {iss['title']}")
        else:
            print(f"  [!] Failed #{num}: {res.stderr.strip()}")
        time.sleep(0.5)

    print("\n[Done] All issue titles synced to open source taxonomy!")

if __name__ == "__main__":
    main()
