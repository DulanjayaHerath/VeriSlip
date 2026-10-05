"""Generate the deterministic issue #95 publication architecture figure."""

from pathlib import Path


OUTPUT = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "research"
    / "figures"
    / "multilayer_architecture.svg"
)


def build_svg() -> str:
    """Return a standalone SVG using only text and vector primitives."""
    boxes = [
        (30, 36, 210, 72, "Sanitized RGB input", "bounded; max dimension 1400"),
        (285, 20, 220, 78, "Layer 1 + 1.5", "structure, metadata, OCR semantics"),
        (285, 118, 220, 78, "Layer 2 + 2.5", "ELA, DCT, copy-move, occlusion"),
        (285, 216, 220, 78, "Layer 3", "residual variance and SRM summaries"),
        (285, 314, 220, 78, "Layer 4 + adjunct", "optional dual stream; rule fallback"),
        (560, 118, 220, 176, "Evidence fusion", "weighted term + gated maxima\nIoU 0.3 region suppression"),
        (835, 118, 220, 176, "Research output", "risk and three-way verdict\nregions, findings, maps"),
    ]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="430" viewBox="0 0 1080 430" role="img" aria-labelledby="title desc">',
        '<title id="title">VeriSlip multi-layer forensic methodology</title>',
        '<desc id="desc">Sanitized input fans out to implemented evidence layers, which feed max-pooled fusion and research outputs.</desc>',
        '<rect width="1080" height="430" fill="#ffffff"/>',
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#334155"/></marker></defs>',
        '<g stroke="#334155" stroke-width="2" fill="none" marker-end="url(#arrow)">',
        '<path d="M240 72 H260 V59 H285"/><path d="M240 72 H260 V157 H285"/>',
        '<path d="M240 72 H260 V255 H285"/><path d="M240 72 H260 V353 H285"/>',
        '<path d="M505 59 H535 V165 H560"/><path d="M505 157 H560"/>',
        '<path d="M505 255 H535 V247 H560"/><path d="M505 353 H535 V275 H560"/>',
        '<path d="M780 206 H835"/></g>',
    ]
    for x, y, width, height, title, detail in boxes:
        fill = "#eff6ff" if x < 560 else "#f0fdf4"
        parts.append(
            f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="8" fill="{fill}" stroke="#1e3a5f" stroke-width="2"/>'
        )
        parts.append(
            f'<text x="{x + width / 2}" y="{y + 27}" text-anchor="middle" font-family="Arial, sans-serif" font-size="16" font-weight="700" fill="#0f172a">{title}</text>'
        )
        for index, line in enumerate(detail.split("\n")):
            parts.append(
                f'<text x="{x + width / 2}" y="{y + 50 + index * 20}" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#334155">{line}</text>'
            )
    parts.extend(
        [
            '<text x="540" y="418" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#475569">Dashed or planned components are intentionally absent; this figure covers executable paths only.</text>',
            "</svg>",
        ]
    )
    return "\n".join(parts) + "\n"


def main() -> int:
    """Write the figure to its documented repository location."""
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(build_svg(), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(Path(__file__).resolve().parents[1])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

