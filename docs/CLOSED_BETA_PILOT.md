# Closed beta merchant pilot kit

This repository contains a **pilot plan and local analysis tooling**, not a
claim that the two-week human pilot has taken place. No merchant was recruited
and no real receipt, phone number, feedback, or result is committed here.

## Objective and scope

Evaluate whether the existing WhatsApp flow is understandable and operationally
useful to up to 10 consenting Sri Lankan Instagram or Facebook Marketplace
sellers over 14 consecutive days. Observe usability, turnaround experience,
false alarms, and missed fraud reports. This is not a clinical-style accuracy
study and must not be marketed as one.

## Eligibility, consent, and withdrawal

Participants must be adults who control a small social-commerce business, can
use WhatsApp, understand that VeriSlip is decision support rather than proof of
payment, and voluntarily sign the pilot consent notice. Exclude anyone unable
to remove third-party data lawfully or who expects automatic dispatch approval.
Participation is unpaid unless the approved protocol says otherwise. A seller
may withdraw at any time; stop collection and delete their linkable pilot data
unless retention is legally required.

Before activation, explain the purpose, 14-day duration, foreseeable false
positive/negative risk, human-review requirement, data categories, retention,
contact route, withdrawal process, and that no sale or partnership is implied.
Record consent outside this repository in an access-controlled system.

## Onboarding and two-week procedure

1. Assign a random local code matching `seller-` plus eight lowercase hex
   characters. Keep the identity-to-code map separately with the pilot lead.
2. Demonstrate `help`, `balance`, language selection, and JPEG/PNG submission.
   Reinforce: check the bank app before dispatch regardless of the verdict.
3. Ask sellers to submit only receipts they are permitted to process. The
   existing WhatsApp path downloads in memory, sanitizes the image, applies
   idempotency and merchant credit controls, and avoids logging raw media.
4. On days 1–14, record only the structured event fields below. Never copy OCR
   text, names, phone numbers, account numbers, references, captions, images, or
   free-form customer messages into the pilot dataset.
5. Check in near days 3, 7, and 14 using a neutral script: “Was the reply clear?
   Was the wait acceptable? Did you independently confirm the outcome?” Use a
   feedback code rather than verbatim customer information.
6. Escalate disputed or high-risk cases to the named human reviewer. Do not ask
   the seller to resend private data by email or issue tracker.

## Structured observation file

Keep the CSV outside Git with this exact header:

```csv
participant_id,pilot_day,event_type,model_verdict,confirmed_outcome,feedback_code
```

Allowed values are enforced by `scripts\analyze_closed_beta.py`. Outcomes are
`genuine`, `fraud`, or `unconfirmed`; only independently confirmed rows enter
false-positive/false-negative counts. Feedback codes are `useful`, `unclear`,
`too_slow`, `false_alarm`, `missed_fraud`, or `other`. Do not add a free-text
column. The tool reports aggregates only and never emits participant IDs.

## Safety, escalation, and stop rules

- A high-risk result or seller dispute requires bank-app confirmation and human
  review before goods are dispatched.
- Pause an individual immediately on consent withdrawal, privacy concern, or
  repeated unsafe reliance on the bot.
- Pause the pilot for a suspected data breach, systematic unsafe advice,
  unavailable escalation owner, or unexplained service instability.
- Notify the security owner through the private incident channel; do not paste
  receipts or identifiers into GitHub, chat logs, or analytics.

## Success criteria and final analysis

Before recruitment, the pilot owner must set numeric targets for completion,
response usefulness, turnaround, and tolerable confirmed error counts. Do not
choose thresholds after observing results. At day 14, report participant and
event counts, completion/withdrawal counts, confirmed-verification coverage,
verdict and coded-feedback distributions, false positives, false negatives,
incidents, and qualitative themes written without identifying examples.
Unconfirmed cases stay visibly unconfirmed.

Delete the identity map and raw operational records on the approved retention
schedule. Retain only consent records where required and anonymized aggregate
results. The local in-memory stores are test-friendly, not durable pilot-study
storage; production operation needs approved encrypted persistence, access
control, backups, deletion workflows, and an incident-response owner.

## Local analysis

```cmd
python scripts\analyze_closed_beta.py C:\secure-pilot\events.csv
python -m pytest tests\test_closed_beta_pilot.py -v
```
