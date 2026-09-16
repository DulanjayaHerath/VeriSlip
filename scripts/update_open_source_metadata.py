#!/usr/bin/env python3
"""
Updates all 100 issues in scripts/issues_data.json and on GitHub
to use clean, professional open-source domain prefixes and contributor guidance.
"""

import os
import json
import subprocess
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ISSUES_FILE = os.path.join(SCRIPT_DIR, "issues_data.json")

ROLE_MAPPINGS = {
    "person1-cv": {
        "prefix": "FORENSICS-CV",
        "domain": "Forensic Computer Vision & Signal Processing",
        "label": "domain:cv-forensics"
    },
    "person2-ml": {
        "prefix": "ML-DATA",
        "domain": "Machine Learning & Dataset Engineering",
        "label": "domain:ml-data"
    },
    "person3-fullstack": {
        "prefix": "BACKEND-API",
        "domain": "Backend Systems & Enterprise Integrations",
        "label": "domain:backend-api"
    },
    "shared": {
        "prefix": "INFRA-RESEARCH",
        "domain": "DevOps, Security & Academic Research",
        "label": "domain:infra-research"
    }
}

def main():
    with open(ISSUES_FILE, "r") as f:
        issues = json.load(f)

    print("Updating local issues_data.json structure...")
    for iss in issues:
        role = iss.get("role", "shared")
        mapping = ROLE_MAPPINGS.get(role, ROLE_MAPPINGS["shared"])
        
        # Clean title
        raw_title = iss["title"]
        for old_tag in ["[PERSON1-CV] ", "[PERSON2-ML] ", "[PERSON3-FULLSTACK] ", "[SHARED] ", "[FORENSICS-CV] "]:
            if raw_title.startswith(old_tag):
                raw_title = raw_title[len(old_tag):]
                break
        
        new_title = f"[{mapping['prefix']}] {raw_title}"
        iss["title"] = new_title
        iss["domain_track"] = mapping["domain"]
        iss["labels"] = [
            mapping["label"],
            f"milestone:{iss['milestone'].split(':')[0].lower().replace(' ', '-')}",
            f"priority:{iss['priority'].lower()}",
            f"layer:{iss['layer'].lower().replace(' ', '-')}",
            "contributions-welcome"
        ]
        
        # Professional open source body
        iss["body"] = f"""### Overview
{iss['body'].split('### Summary')[1].split('### Track & Ownership')[0].strip()}

### Domain & Subsystem
* **Technical Domain:** `{mapping['domain']}`
* **Detection Layer / Component:** `{iss['layer']}`
* **Target Milestone:** `{iss['milestone']}`
* **Difficulty / Priority:** `{iss['priority']}`

### Acceptance Criteria
- [ ] Implement technical specifications described above.
- [ ] Add unit / integration tests in `tests/`.
- [ ] Verify test suite passes (`pytest tests/`).
- [ ] Adhere to project linting and documentation guidelines.
- [ ] Submit PR referencing this issue.
"""

    with open(ISSUES_FILE, "w") as f:
        json.dump(issues, f, indent=2)

    print(f"Updated {len(issues)} local issues in scripts/issues_data.json.")

if __name__ == "__main__":
    main()
