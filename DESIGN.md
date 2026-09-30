# VeriSlip visual system

<!-- impeccable:design-schema 1 -->

## Direction

VeriSlip is a forensic score: a paper-and-ink evidence console for operators who need to move from ingestion to a defensible decision quickly. The visual language borrows from notation and laboratory record systems—clear bilateral inspection, strong baselines, measured labels, and state color reserved for evidence.

## Surface

- Light operational canvas (`--paper`) with a subtle paper grain made from low-contrast dots.
- White working surfaces with one-pixel cool-gray rules and restrained soft elevation.
- Ink-black/navy chrome for trust and code-heavy surfaces.
- Cobalt is the action and selection color; teal, amber, rose, and violet are semantic signal colors only.
- The primary cockpit remains a three-part task: ingestion, evidence view, and decision rail.

## Typography

- UI copy uses the system sans stack for dependable product readability.
- JetBrains Mono is reserved for measurements, risk percentages, code samples, and identifiers.
- Headings use compact negative tracking and a clear step above body copy; labels use uppercase letter-spaced utility styling.

## Components

- `glass-card` is retained as the compatibility class name, but its implementation is an opaque surface with a one-pixel rule, not glass or blur.
- Buttons share an 8px radius, visible focus ring, explicit disabled state, and cobalt primary treatment.
- Input controls share the same rule, radius, padding, and focus language.
- Evidence states are always encoded with label + color + structural cue; color is never the only signal.
- Empty, loading, safe, suspicious, and high-risk states are all styled as first-class product states.

## Responsive behavior

- Desktop uses a 312px ingestion rail, flexible evidence canvas, and 326px verdict rail.
- At tablet widths the cockpit becomes a two-column control grid and the verdict rail becomes a balanced grid.
- At mobile widths all operational regions stack, tabs remain horizontally scrollable, and action groups become full-width.
- Motion is limited to short state transitions and respects `prefers-reduced-motion`.

## Do not regress

- Do not restore gradients, emoji-as-icons, translucent glass decoration, or thick colored side tabs.
- Do not hide the verdict or triage action behind a modal.
- Do not replace product evidence with invented performance claims or decorative metrics.
