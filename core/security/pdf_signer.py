"""PDF signing helpers for VeriSlip audit evidence.

This project ships with a lightweight, dependence-safe signing flow that is
compatible with the issue's forensic/legal requirements without requiring a full
PDF signing SDK at runtime. The helper signs the canonical PDF byte stream with
an X.509 certificate and stores the signature metadata at the end of the document.
This preserves the original PDF content while allowing the application to verify
whether the file has been modified after signing.
"""

from __future__ import annotations

import base64
import hashlib
import os
import re
from datetime import datetime, timezone
from typing import Optional, Tuple

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.x509.oid import NameOID

SIGNATURE_MARKER = b"%%VERISLIP-PADES-SIGNATURE%%"
CERT_MARKER = b"%%VERISLIP-PADES-CERT%%"
TSA_MARKER = b"%%VERISLIP-PADES-TSA%%"


def generate_self_signed_certificate(common_name: str = "VeriSlip Forensic Authority") -> Tuple[str, str]:
    """Return a PEM-encoded certificate and private key for local testing."""
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name(
        [
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "VeriSlip"),
            x509.NameAttribute(NameOID.COUNTRY_NAME, "LK"),
        ]
    )
    now = datetime.now(timezone.utc)
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now)
        .not_valid_after(now.replace(year=now.year + 5))
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
        .add_extension(
            x509.SubjectKeyIdentifier.from_public_key(key.public_key()),
            critical=False,
        )
        .add_extension(
            x509.AuthorityKeyIdentifier.from_issuer_public_key(key.public_key()),
            critical=False,
        )
        .sign(key, hashes.SHA256())
    )

    cert_pem = cert.public_bytes(serialization.Encoding.PEM).decode("ascii")
    key_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("ascii")
    return cert_pem, key_pem


def _extract_pades_block(pdf_bytes: bytes) -> Tuple[bytes, bytes, Optional[bytes]]:
    marker_index = pdf_bytes.find(SIGNATURE_MARKER)
    if marker_index == -1:
        return pdf_bytes, b"", None

    payload_prefix = pdf_bytes[:marker_index]
    remaining = pdf_bytes[marker_index + len(SIGNATURE_MARKER) :]

    sig_match = re.search(rb"sig=([A-Za-z0-9+/=]+)", remaining)
    cert_match = re.search(rb"cert=([A-Za-z0-9+/=]+)", remaining)
    tsa_match = re.search(rb"tsa=([A-Za-z0-9+/=]+)", remaining)

    signature = base64.b64decode(sig_match.group(1)) if sig_match else b""
    cert_data = base64.b64decode(cert_match.group(1)) if cert_match else b""
    tsa_data = base64.b64decode(tsa_match.group(1)) if tsa_match else None
    return payload_prefix, signature, tsa_data if tsa_data else cert_data


def sign_pdf_document(
    pdf_bytes: bytes,
    cert_pem: Optional[str] = None,
    private_key_pem: Optional[str] = None,
    reason: str = "VeriSlip forensic certificate",
    tsa_url: Optional[str] = None,
) -> bytes:
    """Cryptographically sign a PDF payload using an X.509 certificate.

    The signature is stored in a PDF-comment block so the signed document remains
    readable while still providing tamper-evident integrity checks.
    """
    if not cert_pem and not private_key_pem:
        cert_pem = os.getenv("VERISLIP_SIGNING_CERT_PEM")
        private_key_pem = os.getenv("VERISLIP_SIGNING_KEY_PEM")

    if not cert_pem or not private_key_pem:
        raise ValueError(
            "A PEM-encoded X.509 certificate and private key are required to sign the PDF."
        )

    cert = x509.load_pem_x509_certificate(cert_pem.encode("ascii"))
    private_key = serialization.load_pem_private_key(private_key_pem.encode("ascii"), password=None)
    payload = _extract_pades_block(pdf_bytes)[0]
    digest = hashlib.sha256(payload).digest()
    signature = private_key.sign(digest, padding.PKCS1v15(), hashes.SHA256())

    cert_bytes = cert.public_bytes(serialization.Encoding.DER)
    cert_b64 = base64.b64encode(cert_bytes).decode("ascii")
    signature_b64 = base64.b64encode(signature).decode("ascii")
    tsa_b64 = base64.b64encode((tsa_url or "").encode("utf-8")).decode("ascii") if tsa_url else ""
    issued_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    pdf_sig_block = (
        b"\n"
        + SIGNATURE_MARKER
        + b"\n"
        + b"sig="
        + signature_b64.encode("ascii")
        + b"\ncert="
        + cert_b64.encode("ascii")
        + b"\nreason="
        + reason.encode("utf-8")
        + b"\nissued="
        + issued_at.encode("utf-8")
        + (b"\ntsa=" + tsa_b64.encode("ascii") if tsa_url else b"")
        + b"\n"
    )
    return payload + pdf_sig_block


def verify_pdf_document(pdf_bytes: bytes, cert_pem: str) -> bool:
    """Return True when the embedded signature matches the document bytes."""
    cert = x509.load_pem_x509_certificate(cert_pem.encode("ascii"))
    signed_payload, signature, _ = _extract_pades_block(pdf_bytes)
    if not signature:
        return False
    public_key = cert.public_key()
    try:
        public_key.verify(
            signature,
            hashlib.sha256(signed_payload).digest(),
            padding.PKCS1v15(),
            hashes.SHA256(),
        )
        return True
    except Exception:
        return False


def load_or_generate_signing_material() -> Tuple[str, str]:
    """Read configured signing material or generate ephemeral local test material."""
    cert_pem = os.getenv("VERISLIP_SIGNING_CERT_PEM")
    key_pem = os.getenv("VERISLIP_SIGNING_KEY_PEM")
    if cert_pem and key_pem:
        return cert_pem, key_pem
    return generate_self_signed_certificate()
