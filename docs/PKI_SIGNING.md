# PKI signing for VeriSlip forensic PDF certificates

VeriSlip supports optional PDF signing for legal evidence exports. The signing flow accepts a PEM-encoded X.509 certificate and matching private key and appends a cryptographic integrity marker to the generated PDF body.

## Required environment variables

Set the following before generating signed PDFs:

```bash
export VERISLIP_SIGNING_CERT_PEM="$(cat cert.pem)"
export VERISLIP_SIGNING_KEY_PEM="$(cat key.pem)"
```

## Example OpenSSL issuance

```bash
openssl req -x509 -newkey rsa:4096 -sha256 -days 1825 \
  -keyout key.pem -out cert.pem \
  -subj "/CN=VeriSlip Forensic Authority/O=VeriSlip/C=LK" \
  -addext "basicConstraints=CA:FALSE" \
  -addext "keyUsage=digitalSignature,keyEncipherment" \
  -addext "extendedKeyUsage=codeSigning,emailProtection"
```

## API usage

```bash
curl -X POST "http://localhost:8000/api/v1/report/audit-pdf" \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{
    "verdict": "AUTHENTIC",
    "tamper_risk_percentage": 2.1,
    "recommendation": "Proceed with transaction verification.",
    "sign_pdf": true,
    "signature_reason": "Forensic evidence certificate",
    "signing_certificate_pem": "-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----",
    "signing_private_key_pem": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----"
  }'
```

## Legal notes

This implementation preserves the document payload and signs the canonical PDF bytes with SHA-256, enabling tamper detection and an audit trail suitable for internal legal review and forensic evidence handling. For a production deployment, replace the test certificate with a corporate or government-trusted X.509 certificate and store private material in a secure secret manager.
