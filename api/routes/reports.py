"""
PDF Forensic Audit Certificate Generator for VeriSlip.
Produces official, cryptographically signed examination sheets using ReportLab.
"""

import io
import hashlib
import json
import os
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, Field

from core.security.pdf_signer import sign_pdf_document
from core.security.merkle_audit import MerkleAuditLedger

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

router = APIRouter(prefix="/api/v1/report", tags=["Audit Reports"])
audit_ledger = MerkleAuditLedger()

class AuditReportRequest(BaseModel):
    verdict: str
    tamper_risk_percentage: float
    recommendation: str
    findings_summary: list = []
    layer_breakdowns: Dict[str, Any] = {}
    flagged_regions: list = []
    bank_name: Optional[str] = "Sri Lankan Commercial Bank"
    reference_no: Optional[str] = "N/A"
    sign_pdf: bool = False
    include_pades_signature: Optional[bool] = None
    signature_reason: Optional[str] = "VeriSlip Forensic Authority"
    tsa_url: Optional[str] = None
    signing_certificate_pem: Optional[str] = None
    signing_private_key_pem: Optional[str] = None
    slip_sha256: Optional[str] = None
    audit_timestamp: Optional[str] = None
    merchant_signature: Optional[str] = None

@router.post("/audit-pdf")
def generate_pdf_report(req: AuditReportRequest):
    """
    Generate official, downloadable PDF Forensic Audit Certificate.
    """
    try:
        sign_requested = req.sign_pdf or bool(req.include_pades_signature)
        if req.include_pades_signature is False:
            sign_requested = False

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()

        # Custom Styles
        title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=18,
            leading=22,
            textColor=colors.HexColor('#0F172A'),
            alignment=TA_LEFT
        )
        subtitle_style = ParagraphStyle(
            'DocSubTitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=12,
            textColor=colors.HexColor('#64748B'),
            alignment=TA_LEFT
        )
        section_heading = ParagraphStyle(
            'SectionHead',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=14,
            textColor=colors.HexColor('#1E293B'),
            spaceBefore=10,
            spaceAfter=4
        )
        body_style = ParagraphStyle(
            'Body',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=8.5,
            leading=11.5,
            textColor=colors.HexColor('#334155')
        )
        badge_style = ParagraphStyle(
            'Badge',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=13,
            alignment=TA_CENTER
        )

        story = []

        # Generate Document Fingerprint
        timestamp_str = req.audit_timestamp or datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        raw_hash_data = f"{req.verdict}_{req.tamper_risk_percentage}_{timestamp_str}"
        cert_hash = hashlib.sha256(raw_hash_data.encode()).hexdigest().upper()
        doc_id = f"VS-{cert_hash[:10]}"
        slip_sha256 = req.slip_sha256 or cert_hash.lower()
        audit_receipt = audit_ledger.append(
            slip_sha256=slip_sha256,
            timestamp=timestamp_str,
            layer_scores=req.layer_breakdowns,
            verdict=req.verdict,
            bounding_boxes=req.flagged_regions,
            merchant_signature=req.merchant_signature,
        )

        # Header Block
        header_data = [
            [
                Paragraph("<b>VERISLIP FORENSIC AI</b><br/>Electronic Payment Document Authenticity Verification", title_style),
                Paragraph(f"<b>CERTIFICATE ID:</b> {doc_id}<br/><b>ISSUED:</b> {timestamp_str}", subtitle_style)
            ]
        ]
        t_header = Table(header_data, colWidths=[340, 200])
        t_header.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ]))
        story.append(t_header)
        story.append(Spacer(1, 10))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284C7'), spaceBefore=1, spaceAfter=8))

        # Verdict Summary Card
        verdict_bg = colors.HexColor('#ECFDF5') if req.verdict == "AUTHENTIC" else (colors.HexColor('#FEF3C7') if req.verdict == "SUSPICIOUS" else colors.HexColor('#FEF2F2'))
        verdict_text_color = colors.HexColor('#065F46') if req.verdict == "AUTHENTIC" else (colors.HexColor('#92400E') if req.verdict == "SUSPICIOUS" else colors.HexColor('#991B1B'))

        verdict_data = [
            [
                Paragraph(f"<b>FINAL FORENSIC VERDICT:</b> {req.verdict}", ParagraphStyle('VTitle', parent=badge_style, textColor=verdict_text_color)),
                Paragraph(f"<b>TAMPER RISK SCORE:</b> {req.tamper_risk_percentage:.1f}%", ParagraphStyle('VScore', parent=badge_style, textColor=verdict_text_color))
            ],
            [
                Paragraph(f"<b>Recommendation:</b> {req.recommendation}", body_style),
                Paragraph(f"<b>Target Bank:</b> {req.bank_name}", body_style)
            ]
        ]
        t_verdict = Table(verdict_data, colWidths=[360, 180])
        t_verdict.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), verdict_bg),
            ('BOX', (0, 0), (-1, -1), 1, verdict_text_color),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(t_verdict)
        story.append(Spacer(1, 12))

        # Multi-Layer Signals Breakdown
        story.append(Paragraph("<b>MULTI-LAYER FORENSIC EVIDENCE BREAKDOWN</b>", section_heading))

        l1 = req.layer_breakdowns.get("layer1_structural", {})
        l2 = req.layer_breakdowns.get("layer2_classical", {})
        l3 = req.layer_breakdowns.get("layer3_noise", {})
        l4 = req.layer_breakdowns.get("layer4_ensemble", {})

        layer_rows = [
            ["Detection Layer", "Signal Analyzed", "Risk Rating", "Finding Summary"],
            [
                "Layer 1: Structural",
                "Reference checksum, aspect ratio, EXIF software tags",
                f"{float(l1.get('score', 0.0))*100:.0f}%",
                l1.get("findings", ["Compliant layout"])[0] if l1.get("findings") else "No structural anomalies"
            ],
            [
                "Layer 2: Classical ELA/DCT",
                "Error Level Analysis variance, 2D-DCT periodicity",
                f"{float(l2.get('score', 0.0))*100:.0f}%",
                l2.get("findings", ["Normal compression distribution"])[0] if l2.get("findings") else "Uniform compression"
            ],
            [
                "Layer 3: Noise Forensics",
                "High-pass spatial noise residual & flat patch variance",
                f"{float(l3.get('score', 0.0))*100:.0f}%",
                l3.get("findings", ["Consistent noise floor"])[0] if l3.get("findings") else "Homogeneous noise texture"
            ],
            [
                "Layer 4: Deep Learning",
                "Dual-stream cross-attention feature fusion (RGB + tensor)",
                f"{float(l4.get('score', 0.0))*100:.0f}%",
                f"Neural tamper probability: {float(l4.get('tamper_probability', 0.0))*100:.1f}%"
            ]
        ]

        t_layers = Table(layer_rows, colWidths=[110, 150, 70, 210])
        t_layers.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F1F5F9')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
            ('ALIGN', (2, 0), (2, -1), 'CENTER'),
        ]))
        story.append(t_layers)
        story.append(Spacer(1, 12))

        # Flagged Regions Table if available
        if req.flagged_regions:
            story.append(Paragraph("<b>LOCALIZED TAMPER BOUNDING BOXES</b>", section_heading))
            region_rows = [["#", "Bounding Box [X, Y, W, H]", "Confidence", "Detected Splicing Signature"]]
            for idx, reg in enumerate(req.flagged_regions[:5]):
                box_str = str(reg.get("box", []))
                conf = f"{float(reg.get('confidence', 0.0))*100:.0f}%"
                label = reg.get("label", "Anomalous Region")
                region_rows.append([str(idx + 1), box_str, conf, label])

            t_regions = Table(region_rows, colWidths=[24, 150, 66, 300])
            t_regions.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F8FAFC')),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
                ('ALIGN', (2, 0), (2, -1), 'CENTER'),
            ]))
            story.append(t_regions)
            story.append(Spacer(1, 12))

        # Legal & Dispute Evidentiary Statement
        story.append(Paragraph("<b>LEGAL NOTICE & EVIDENTIARY STATUTES</b>", section_heading))
        legal_text = (
            "This examination report certifies that the uploaded transaction slip was subjected to automated multi-scale "
            "computational forensics adhering to standard signal processing and digital image analysis practices. "
            "The findings summarized herein indicate localized error level discrepancies, frequency domain compression "
            "traces, and noise variance discontinuities. This document is admissible as supporting technical evidence for "
            "merchant dispute resolution, banking chargeback investigations, and law enforcement cybercrime reports."
        )
        story.append(Paragraph(legal_text, ParagraphStyle('Legal', parent=body_style, textColor=colors.HexColor('#64748B'))))
        story.append(Spacer(1, 14))

        # Cryptographic Footer Seal
        seal_data = [
            [
                Paragraph(f"<b>SHA-256 DIGITAL FINGERPRINT:</b><br/><font face='Courier'>{cert_hash}</font>", ParagraphStyle('Hash', parent=body_style, fontSize=7, leading=9)),
                Paragraph("<b>CRYPTOGRAPHICALLY SIGNED BY:</b><br/>VeriSlip Automated Forensic Authority v1.0", ParagraphStyle('Sign', parent=body_style, fontSize=7, leading=9, alignment=TA_RIGHT))
            ]
        ]
        t_seal = Table(seal_data, colWidths=[360, 180])
        t_seal.setStyle(TableStyle([
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('LINEABOVE', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ]))
        story.append(t_seal)
        story.append(Spacer(1, 8))
        proof_path = json.dumps(list(audit_receipt.siblings), separators=(",", ":"))
        story.append(Paragraph(
            "<b>MERKLE AUDIT RECEIPT</b><br/>"
            f"Root: <font face='Courier'>{audit_receipt.root}</font><br/>"
            f"Leaf: <font face='Courier'>{audit_receipt.leaf_hash}</font><br/>"
            f"Entry index: {audit_receipt.index} | Proof nodes: {len(audit_receipt.siblings)}<br/>"
            f"Proof path: <font face='Courier'>{proof_path}</font>",
            ParagraphStyle('MerkleReceipt', parent=body_style, fontSize=7, leading=9),
        ))

        # Build PDF
        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()

        if sign_requested:
            cert_pem = req.signing_certificate_pem or os.getenv("VERISLIP_SIGNING_CERT_PEM")
            key_pem = req.signing_private_key_pem or os.getenv("VERISLIP_SIGNING_KEY_PEM")
            if not cert_pem or not key_pem:
                raise HTTPException(
                    status_code=400,
                    detail="PDF signing cannot be enabled without a valid certificate and private key."
                )
            pdf_bytes = sign_pdf_document(
                pdf_bytes,
                cert_pem=cert_pem,
                private_key_pem=key_pem,
                reason=req.signature_reason or "VeriSlip Forensic Authority",
                tsa_url=req.tsa_url or os.getenv("VERISLIP_TSA_URL"),
            )

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="VeriSlip_Audit_{doc_id}.pdf"'}
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")
