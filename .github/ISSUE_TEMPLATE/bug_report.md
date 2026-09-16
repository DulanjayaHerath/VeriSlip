---
name: Bug Report / False Positive Report
about: Report a false positive, detection failure, or API issue
title: "[BUG] "
labels: ["bug"]
assignees: ""
---

### Describe the Bug / Detection Failure
A clear description of what went wrong (e.g. genuine payment slip flagged as tampered, or doctored amount missed).

### Slip Information
* **Bank Name / App:** [e.g. Commercial Bank ComBank Digital, Sampath Vishwa, BOC, HNB]
* **Operating System / Source:** [e.g. Android 14 screenshot, iOS 18 screenshot, forwarded WhatsApp Web image]
* **Actual Slip Status:** [Authentic / Tampered]

### Observed Scores vs Expected
* **Tamper Risk Score Observed:** [e.g. 85%]
* **Expected Risk Score:** [e.g. < 20%]
* **Flagged Regions:** [e.g. False anomaly box around checkmark]

### Steps to Reproduce
1. Upload slip image to `/api/v1/verify` or via Web Cockpit.
2. Select Bank Template `...`.
3. View output risk assessment and layer breakdown.
