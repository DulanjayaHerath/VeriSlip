"""TAXII 2.1 and STIX 2.1 threat-intelligence feed routes."""

from __future__ import annotations

import os
import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Request

from core.threat_intel.stix_exporter import get_default_verislip_bundle

router = APIRouter(tags=["Threat Intelligence"])

_COLLECTION_ID = "verislip-fraud-indicators"


def _get_expected_token() -> str | None:
    return os.getenv("TAXII_API_TOKEN") or os.getenv("VERISLIP_TAXII_TOKEN")


def _require_auth(request: Request) -> None:
    expected_token = _get_expected_token()
    if not expected_token:
        return

    auth_header = request.headers.get("authorization") or request.headers.get("x-api-key") or request.headers.get("x-taxii-api-key")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing TAXII API token.")

    if auth_header.lower().startswith("bearer "):
        token = auth_header.split(" ", 1)[1].strip()
    else:
        token = auth_header.strip()

    if token != expected_token:
        raise HTTPException(status_code=401, detail="Invalid TAXII API token.")


@router.get("/taxii2/collections")
async def list_taxii_collections(request: Request):
    """List the available TAXII collections for subscriber discovery."""
    _require_auth(request)
    return {
        "collections": [
            {
                "id": f"x-collection--{uuid.uuid4()}",
                "name": "VeriSlip Fraud Indicators",
                "type": "Collection",
                "spec_version": "2.1",
                "description": "Anonymized bank-slip fraud indicators distributed to participating institutions.",
                "media_types": ["application/vnd.oasis.stix+json", "application/vnd.oasis.taxii+json"],
            }
        ]
    }


@router.get(f"/taxii2/collections/{_COLLECTION_ID}/")
async def get_taxii_collection(request: Request):
    """Return the TAXII collection metadata plus the current STIX objects."""
    _require_auth(request)
    bundle = get_default_verislip_bundle()
    return {
        "type": "Collection",
        "id": f"x-collection--{uuid.uuid4()}",
        "spec_version": "2.1",
        "name": "VeriSlip Fraud Indicators",
        "description": "Anonymized indicators of compromise for forged bank slips and payment scams.",
        "media_types": ["application/vnd.oasis.stix+json", "application/vnd.oasis.taxii+json"],
        "objects": bundle["objects"],
    }


@router.get(f"/taxii2/collections/{_COLLECTION_ID}/objects/")
async def get_taxii_collection_objects(request: Request):
    """Return the STIX bundle for the fraud threat intelligence feed."""
    _require_auth(request)
    return get_default_verislip_bundle()


__all__ = ["router"]
