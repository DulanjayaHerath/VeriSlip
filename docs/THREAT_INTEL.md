# Threat Intelligence Integration Guide

This guide describes how VeriSlip publishes anonymized fraud intelligence using the STIX 2.1 and TAXII 2.1 standards.

## Collection endpoint

The feed is exposed via the TAXII collection endpoint:

- `GET /taxii2/collections/verislip-fraud-indicators/`
- `GET /taxii2/collections/verislip-fraud-indicators/objects/`

The collection returns a STIX 2.1 `bundle` object containing `indicator`, `observed-data`, and `relationship` objects that describe forged slip templates and syndicate activity without exposing individual account numbers.

## Authorization

If you want to require a token for enterprise subscribers, set one of the following environment variables before startup:

- `TAXII_API_TOKEN`
- `VERISLIP_TAXII_TOKEN`

Then send the value as either a bearer token or an `X-API-Key` header.

## Consumers

The feed is intended for Sri Lanka CERT|CC, the Central Bank Financial Intelligence Unit (FIU), and participating member banks that operate automated security monitoring pipelines.

## Example response

```json
{
  "type": "bundle",
  "spec_version": "2.1",
  "objects": [
    {
      "type": "indicator",
      "pattern": "[file:hashes.'SHA-256' = '...']",
      "pattern_type": "stix",
      "labels": ["fraud", "banking-fraud"]
    }
  ]
}
```
