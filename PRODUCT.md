# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Existing vanilla HTML, CSS, and JavaScript frontend served by the existing FastAPI application. No framework migration is planned for this visual redesign.

## Users

Assumption for this pass: merchant operations teams, marketplace sellers, and support staff who need to verify payment slips quickly and make an accept-or-flag decision.

## Product Purpose

VeriSlip checks Sri Lankan bank transfer slips and payment receipts for signs of tampering. The frontend should help an operator ingest a slip, inspect the evidence, understand the risk, and record a fast triage decision.

## Positioning

VeriSlip combines multiple forensic signals—structural and metadata checks, compression analysis, noise residuals, and a deep-learning ensemble—into an explainable verification workflow rather than presenting a single opaque fraud score.

## Operating Context

Operators work from screenshots or PDFs shared through peer-to-peer commerce, seller support, courier workflows, WhatsApp, or API integrations. The product includes single-slip analysis, batch auditing, WhatsApp simulation, developer API examples, pricing information, and authenticated verification history.

## Capabilities and Constraints

- Preserve the existing single-slip, batch, WhatsApp, API, pricing, and history surfaces and their current element IDs and behavior.
- Preserve keyboard shortcuts for view switching, zoom, scan, and merchant triage.
- Preserve current API-key handling and safe history rendering.
- The primary launch target is desktop and mobile web.
- The interface must make empty, loading, disabled, success, suspicious, and high-risk states legible.
- Existing analysis labels and demo values are product content; do not invent new performance claims.

## Brand Commitments

The product name is VeriSlip. Existing brand language is forensic, operational, and evidence-led. The current shield mark and bank-slip subject matter may be retained, but the visual system may be replaced for shipping quality.

## Evidence on Hand

Existing sample slips are available under `web/samples/`, including authentic and tampered examples from ComBank, Sampath, People's Bank, BOC, and Seylan. Current HTML and JavaScript define the supported flows and labels.

## Product Principles

1. Show evidence before decoration.
2. Make the next operator action obvious.
3. Separate measured signal from interpretation.
4. Preserve trust through honest states and restrained visual emphasis.
5. Keep the fastest path usable on a phone as well as a desktop.

## Accessibility & Inclusion

Use semantic buttons and form controls, visible keyboard focus, sufficient contrast, reduced-motion support, and state cues that do not rely on color alone.
