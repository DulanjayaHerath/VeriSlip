# Permission-cleared genuine benchmark curation

Issue #40 targets 200 genuine slips across iOS and Android. This repository
currently contains **0 permission-cleared curated genuine samples**. This change
provides the safe workflow and tooling needed to collect them; it does not
fabricate images, consent, diversity, or completion.

## Workflow

1. Obtain explicit permission for research use and store the consent evidence
   in an approved access-controlled system outside Git.
2. Place a candidate temporarily in a private intake location. Never use scraped
   receipts, public screenshots, or synthetic images labelled as genuine.
3. Prepare a metadata JSON file containing only the constrained fields below.
4. Run `add`. The tool validates actual JPEG/PNG content with the shared image
   sanitizer, strips metadata, runs the existing local OCR/PII redaction
   pipeline, writes only a generated-name PNG, and records non-identifying
   provenance. Failed redaction exports nothing.
5. Remove the intake copy according to the approved retention policy.
6. Run `finalize` to create the existing deterministic SHA-256 integrity
   manifest. Verify it with `scripts\verify_dataset.py` before evaluation.

Required metadata keys are `bank_category`, `source_type`, `os_family`,
`capture_type`, `permission_status`, and `permission_record_id`. Permission must
be `granted`. The record ID is a pseudonymous pointer to external evidence, not
a person name, phone number, account, transaction reference, or file path.

Allowed source types are `team_transaction` and `merchant_contribution`.
Supported OS families are `ios`, `android`, and `other`; capture types are
`screenshot`, `camera_photo`, and `digital_export`. Bank categories use a small
controlled vocabulary with `other` for an unlisted bank.

## Windows CMD usage

```cmd
python scripts\curate_genuine_benchmark.py add C:\private-intake\candidate.png C:\private-intake\candidate.json C:\private-curated\verislip-genuine
python scripts\curate_genuine_benchmark.py finalize C:\private-curated\verislip-genuine
python scripts\verify_dataset.py verify C:\private-curated\verislip-genuine C:\private-curated\verislip-genuine\integrity_manifest.json
python scripts\curate_genuine_benchmark.py status C:\private-curated\verislip-genuine
```

The curated directory still contains sensitive research material even after
redaction. Keep it out of Git, encrypt it at rest, restrict access, log access
without PII, and honor withdrawal/deletion requests. Local OCR can miss PII;
every candidate needs human privacy review before dataset release. A checksum
detects later byte changes but does not prove consent, authenticity, or label
quality.
