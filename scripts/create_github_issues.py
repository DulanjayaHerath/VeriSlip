#!/usr/bin/env python3
"""
Automated GitHub Issue Creator for VeriSlip.
Imports the 100 structured issues from scripts/issues_data.json into a GitHub repository.

Usage:
  # Dry run (preview issues without creating)
  python3 scripts/create_github_issues.py --dry-run

  # Create issues using GitHub CLI (gh)
  python3 scripts/create_github_issues.py --repo YOUR_USERNAME/VeriSlip

  # Create issues using GitHub Personal Access Token (GITHUB_TOKEN env variable)
  GITHUB_TOKEN=ghp_xxx python3 scripts/create_github_issues.py --repo YOUR_USERNAME/VeriSlip
"""

import os
import sys
import json
import time
import argparse
import subprocess
import urllib.request
import urllib.error

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ISSUES_FILE = os.path.join(SCRIPT_DIR, "issues_data.json")

LABEL_COLORS = {
    # Roles
    "role:person1-cv": "1d76db",        # Deep Blue
    "role:person2-ml": "7057ff",        # Purple
    "role:person3-fullstack": "0e8a16", # Green
    "role:shared": "5319e7",            # Indigo
    # Milestones
    "milestone:phase-1": "fbca04",      # Yellow
    "milestone:phase-2": "fef2c0",      # Light Yellow
    "milestone:phase-3": "c2e0c6",      # Light Green
    "milestone:phase-4": "bfdadc",      # Slate
    # Priorities
    "priority:low": "0075ca",           # Blue
    "priority:medium": "e99695",        # Orange
    "priority:high": "d93f0b",          # Crimson
    # Layers
    "layer:layer-1": "006b75",
    "layer:layer-2": "1d76db",
    "layer:layer-3": "5319e7",
    "layer:layer-4": "b60205",
    "layer:synthetic-data": "0e8a16",
    "layer:dataset": "0052cc",
    "layer:backend-api": "fbca04",
    "layer:whatsapp-bot": "25d366",
    "layer:web-frontend": "1f883d",
    "layer:courier-b2b": "e99695",
    "layer:e-commerce": "d4c5f9",
    "layer:audit-report": "c5def5",
    "layer:monetization": "f9d0c4",
    "layer:devops": "333333",
    "layer:security": "d93f0b",
    "layer:research-paper": "6f42c1",
    "layer:gtm-&-pilot": "bfdadc"
}

def ensure_labels_exist(repo: str):
    """Pre-create all necessary labels with appropriate colors."""
    print("  Ensuring label taxonomy exists on GitHub repo...")
    for label, color in LABEL_COLORS.items():
        cmd = ["gh", "label", "create", label, "--repo", repo, "--color", color, "--force"]
        subprocess.run(cmd, capture_output=True, text=True)
    print("  [✓] Labels configured.")

def create_issue_gh_cli(repo: str, issue: dict) -> bool:
    """Create issue using GitHub CLI (`gh`)."""
    cmd = [
        "gh", "issue", "create",
        "--repo", repo,
        "--title", issue["title"],
        "--body", issue["body"]
    ]
    for label in issue.get("labels", []):
        cmd.extend(["--label", label])

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"  [✓] Created #{issue['number']}: {issue['title']} -> {res.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  [!] Failed #{issue['number']}: {e.stderr.strip()}")
        return False

def create_issue_api(repo: str, token: str, issue: dict) -> bool:
    """Create issue using GitHub REST API."""
    url = f"https://api.github.com/repos/{repo}/issues"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "VeriSlip-Issue-Creator"
    }
    payload = {
        "title": issue["title"],
        "body": issue["body"],
        "labels": issue.get("labels", [])
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"  [✓] Created: {data.get('html_url')}")
            return True
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        print(f"  [!] HTTP {e.code} for #{issue['number']}: {err_msg}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Create 100 GitHub issues for VeriSlip repository.")
    parser.add_argument("--repo", help="Target GitHub repository (e.g. owner/VeriSlip)")
    parser.add_argument("--dry-run", action="store_true", help="Preview issues without creating them")
    parser.add_argument("--limit", type=int, default=100, help="Maximum number of issues to create (default: 100)")
    parser.add_argument("--start", type=int, default=1, help="Start from issue number (1-100)")
    args = parser.parse_args()

    if not os.path.exists(ISSUES_FILE):
        print(f"Error: Could not find {ISSUES_FILE}")
        sys.exit(1)

    with open(ISSUES_FILE, "r") as f:
        issues = json.load(f)

    selected_issues = [i for i in issues if args.start <= i["number"] < (args.start + args.limit)]

    print(f"==================================================")
    print(f"  VeriSlip GitHub Issue Generator (Total: {len(selected_issues)})")
    print(f"==================================================")

    if args.dry_run:
        print("\n[DRY RUN MODE] Previewing first 5 issues:\n")
        for iss in selected_issues[:5]:
            print(f"Issue #{iss['number']}: {iss['title']}")
            print(f"  Role: {iss['role']} | Milestone: {iss['milestone']} | Priority: {iss['priority']}")
            print(f"  Labels: {', '.join(iss['labels'])}\n")
        print(f"... and {len(selected_issues) - 5} more issues ready in {ISSUES_FILE}.")
        print("\nTo create them on your repo, run:")
        print("  gh auth login")
        print(f"  python3 scripts/create_github_issues.py --repo YOUR_ORG/YOUR_REPO")
        return

    if not args.repo:
        print("Error: --repo is required unless running in --dry-run mode.")
        print("Example: python3 scripts/create_github_issues.py --repo yourusername/VeriSlip")
        sys.exit(1)

    token = os.environ.get("GITHUB_TOKEN")
    use_api = bool(token)
    method_name = "GitHub REST API" if use_api else "GitHub CLI (gh)"
    print(f"Target Repo: {args.repo}")
    print(f"Method: {method_name}")
    print(f"Creating {len(selected_issues)} issues...")

    if not use_api:
        ensure_labels_exist(args.repo)

    success_count = 0
    for idx, iss in enumerate(selected_issues):
        print(f"[{idx+1}/{len(selected_issues)}] Processing #{iss['number']}...")
        if use_api:
            ok = create_issue_api(args.repo, token, iss)
        else:
            ok = create_issue_gh_cli(args.repo, iss)
        
        if ok:
            success_count += 1
        time.sleep(1.0) # Avoid secondary rate limits

    print(f"\n[Done] Successfully created {success_count}/{len(selected_issues)} issues on {args.repo}!")

if __name__ == "__main__":
    main()
