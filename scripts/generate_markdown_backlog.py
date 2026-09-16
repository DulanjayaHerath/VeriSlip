#!/usr/bin/env python3
"""
Generates docs/ISSUES_BACKLOG.md from scripts/issues_data.json.
"""

import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
ISSUES_FILE = os.path.join(SCRIPT_DIR, "issues_data.json")
OUTPUT_FILE = os.path.join(ROOT_DIR, "docs", "ISSUES_BACKLOG.md")

def main():
    with open(ISSUES_FILE, "r") as f:
        issues = json.load(f)

    lines = [
        "# VeriSlip: 100 Engineering & Venture Issues Backlog",
        "",
        "This backlog outlines **100 actionable, prioritized issues** divided across the 3 founder roles and shared engineering tracks for collaborative development on GitHub.",
        "",
        "---",
        "",
        "## 👥 Track & Ownership Summary",
        "",
        "| Track | Primary Role | Issues Range | Focus Area |",
        "| :--- | :--- | :--- | :--- |",
        "| **Stream 1** | **Person 1: Forensic CV Lead** | Issues #1 – #28 | Layers 1–3: Bank Templates, ELA, DCT, Noise Residuals, Splicing |",
        "| **Stream 2** | **Person 2: Data & ML Lead** | Issues #29 – #56 | Synthetic Generator, PII Redaction, Layer 4 Deep Learning Ensemble |",
        "| **Stream 3** | **Person 3: Full-Stack & Biz Lead** | Issues #57 – #82 | FastAPI Server, Web Cockpit, WhatsApp Bot, Courier API, Monetization |",
        "| **Stream 4** | **Shared Engineering & Research** | Issues #83 – #100 | CI/CD, Docker, Security/Ethics, Research Paper, Seller Pilot, Layer 5 |",
        "",
        "---",
        "",
        "## 🚀 How to Batch Import into GitHub",
        "",
        "1. Authenticate GitHub CLI:",
        "   ```bash",
        "   gh auth login",
        "   ```",
        "2. Run the automated issue creator script:",
        "   ```bash",
        "   python3 scripts/create_github_issues.py --repo YOUR_GITHUB_USERNAME/VeriSlip",
        "   ```",
        "   *(Or preview first with `python3 scripts/create_github_issues.py --dry-run`)*",
        "",
        "---",
        "",
        "## 📋 Complete List of 100 Issues",
        ""
    ]

    for iss in issues:
        num = iss["number"]
        if num == 1:
            lines.extend(["### 🔬 Stream 1: Person 1 — Forensic Computer Vision (Issues #1 to #28)", ""])
        elif num == 29:
            lines.extend(["", "---", "", "### 🧠 Stream 2: Person 2 — Data Engineering & Deep Learning (Issues #29 to #56)", ""])
        elif num == 57:
            lines.extend(["", "---", "", "### 🌐 Stream 3: Person 3 — Backend, Product & Monetization (Issues #57 to #82)", ""])
        elif num == 83:
            lines.extend(["", "---", "", "### ⚙️ Stream 4: Shared Systems, DevOps, Research Paper & Pilot (Issues #83 to #100)", ""])

        lines.append(f"#### #{iss['number']}: {iss['title']}")
        lines.append(f"* **Role:** `{iss['role']}` | **Layer:** `{iss['layer']}` | **Milestone:** `{iss['milestone']}` | **Priority:** `{iss['priority']}`")
        lines.append(f"* **Labels:** `{', '.join(iss['labels'])}`")
        lines.append("")
        lines.append(iss["body"])
        lines.append("")

    with open(OUTPUT_FILE, "w") as f:
        f.write("\n".join(lines))

    print(f"Saved {len(issues)} issues to {OUTPUT_FILE} successfully!")

if __name__ == "__main__":
    main()
