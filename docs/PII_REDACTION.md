# Receipt image PII redaction

VeriSlip can remove sensitive pixels from real JPEG and PNG receipts before
they are stored in a research dataset. Processing is local: no image or OCR
text is sent to an external service.

## Detection and privacy model

The pipeline has three independently testable stages:

1. The existing local OCR extractor supplies text and bounding boxes.
2. Deterministic rules classify Sri Lankan phone numbers and NICs, plus
   explicitly labelled account numbers and person names. Account/name context
   is required so amounts, dates, times, totals, references, and other ordinary
   receipt numbers are not masked merely because they contain digits.
3. Bounding boxes are clipped to the image and their pixels are replaced with
   a solid black mask (default) or strong Gaussian blur.

Detection results contain only a PII category and location. Recognized values
are not retained or logged. Output is detached RGB PNG pixel data with metadata
removed by the existing image sanitizer and the redaction renderer.

## Dataset command

Run from the repository root. The destination must be separate and existing
outputs are never overwritten:

```text
python scripts\redact_receipts.py datasets\incoming datasets\redacted
python scripts\redact_receipts.py receipt.jpg datasets\redacted --method blur
```

The command accepts one image or the immediate JPEG/PNG files in a directory.
It reports aggregate exported/rejected counts only, avoiding sensitive file
names and OCR values. Invalid images, malformed OCR, unavailable OCR, and
images where local OCR finds no text are rejected without an output file.

Real-slip calibration can instead redact loaded samples in memory:

```text
python scripts\calibrate_real_slips.py --redact-pii
python scripts\calibrate_real_slips.py --redact-pii --redaction-method blur
```

The flag is opt-in for backward compatibility. With it enabled, calibration
stops if OCR/redaction cannot complete.

## Limitations

- OCR quality determines which regions can be found. Fail-closed behavior
  prevents an unreadable image from being exported, but every exported image
  should still receive human privacy review before publication.
- Names are detected only after clear labels such as `Name`, `Customer Name`,
  or `Beneficiary Name`; unlabelled names may remain.
- Account numbers require an account label. Unlabelled identifiers and unusual
  local formats may remain, while a labelled numeric value may be conservatively
  masked.
- The CLI processes images only. PDF receipts should be rendered through the
  project's bounded PDF workflow before redaction.
- Blur is intentionally strong, but solid masking is preferred when irreversible
  removal is required.
