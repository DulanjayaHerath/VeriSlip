"""Construct STIX 2.1 bundles for VeriSlip fraud indicators."""

from __future__ import annotations

from datetime import datetime, timezone
import uuid
from typing import Any, Iterable, Mapping, Sequence

try:  # pragma: no cover - dependency is optional at import-time
    from stix2 import v21  # type: ignore
except Exception:  # pragma: no cover - fallback when stix2 is not installed
    v21 = None


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _make_id(prefix: str) -> str:
    return f"{prefix}--{uuid.uuid4()}"


def _coerce_object_list(objs: Sequence[Mapping[str, Any]] | Iterable[Mapping[str, Any]] | None) -> list[Mapping[str, Any]]:
    if objs is None:
        return []
    return list(objs)


def _serialize_with_stix2(obj: Mapping[str, Any]) -> Mapping[str, Any]:
    if v21 is None:
        return dict(obj)
    factory = {
        "indicator": v21.Indicator,
        "observed-data": v21.ObservedData,
        "threat-actor": v21.ThreatActor,
        "relationship": v21.Relationship,
        "malware": v21.Malware,
        "campaign": v21.Campaign,
    }.get(obj.get("type"))
    if factory is None:
        return dict(obj)
    try:
        result = factory(**{k: v for k, v in obj.items() if k not in {"type", "id"}}).serialize()
        if isinstance(result, str):
            import json
            return json.loads(result)
        return result
    except Exception:
        return dict(obj)


def build_indicator(
    name: str,
    description: str,
    pattern: str,
    labels: Sequence[str] | None = None,
    **extra: Any,
) -> dict[str, Any]:
    indicator = {
        "type": "indicator",
        "spec_version": "2.1",
        "id": _make_id("indicator"),
        "created": _utc_now(),
        "modified": _utc_now(),
        "name": name,
        "description": description,
        "indicator_types": ["malicious-activity"],
        "pattern": pattern,
        "pattern_type": "stix",
        "pattern_version": "2.1",
        "valid_from": _utc_now(),
        "labels": list(labels or ["fraud"]) + extra.pop("labels", []),
        **extra,
    }
    return _serialize_with_stix2(indicator)


def build_observed_data(
    first_observed: str | None = None,
    last_observed: str | None = None,
    number_observed: int = 1,
    objects: Sequence[Mapping[str, Any]] | None = None,
    **extra: Any,
) -> dict[str, Any]:
    observed = {
        "type": "observed-data",
        "spec_version": "2.1",
        "id": _make_id("observed-data"),
        "created": _utc_now(),
        "modified": _utc_now(),
        "first_observed": first_observed or _utc_now(),
        "last_observed": last_observed or _utc_now(),
        "number_observed": number_observed,
        "objects": {f"0:{index}": obj for index, obj in enumerate(_coerce_object_list(objects))},
        **extra,
    }
    return _serialize_with_stix2(observed)


def build_threat_actor(name: str, description: str, aliases: Sequence[str] | None = None, **extra: Any) -> dict[str, Any]:
    actor = {
        "type": "threat-actor",
        "spec_version": "2.1",
        "id": _make_id("threat-actor"),
        "created": _utc_now(),
        "modified": _utc_now(),
        "name": name,
        "description": description,
        "aliases": list(aliases or []),
        "threat_actor_types": ["crime-syndicate"],
        **extra,
    }
    return _serialize_with_stix2(actor)


def build_relationship(source_ref: str, target_ref: str, relationship_type: str, **extra: Any) -> dict[str, Any]:
    rel = {
        "type": "relationship",
        "spec_version": "2.1",
        "id": _make_id("relationship"),
        "created": _utc_now(),
        "modified": _utc_now(),
        "relationship_type": relationship_type,
        "source_ref": source_ref,
        "target_ref": target_ref,
        **extra,
    }
    return _serialize_with_stix2(rel)


def build_stix_bundle(
    indicators: Sequence[Mapping[str, Any]] | None = None,
    observed_data: Sequence[Mapping[str, Any]] | None = None,
    threat_actors: Sequence[Mapping[str, Any]] | None = None,
    relationships: Sequence[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    bundle_objects: list[Mapping[str, Any]] = []
    bundle_objects.extend(_coerce_object_list(indicators))
    bundle_objects.extend(_coerce_object_list(observed_data))
    bundle_objects.extend(_coerce_object_list(threat_actors))
    bundle_objects.extend(_coerce_object_list(relationships))

    if not bundle_objects:
        bundle_objects = [
            build_indicator(
                name="VeriSlip forged slip template cluster",
                description="Forged bank transfer slip templates being reused across e-commerce sellers and merchants.",
                pattern="[file:hashes.'SHA-256' = 'd41d8cd98f00b204e9800998ecf8427e4961d5f2c5e5c1d1f1d98d6c4f906d6f'] OR [url:value LIKE 'https://%/assets/%/bank-slip-%']",
                labels=["fraud", "banking-fraud", "credential-theft"],
            ),
            build_threat_actor(
                name="VeriSlip Fraud Syndicate",
                description="Organized financial fraud operation distributing forged payment slips across multiple commercial sectors.",
                aliases=["SL-FRAUD-01", "Payment Slip Ring"],
            ),
            build_observed_data(
                first_observed=_utc_now(),
                last_observed=_utc_now(),
                number_observed=3,
                objects=[
                    {"type": "account", "account_number": "***-***-1234"},
                    {"type": "domain", "value": "shopbuilder-portal.example"},
                    {"type": "email", "value": "merchant-ops@fraud.example"},
                ],
            ),
        ]
        indicator_id = bundle_objects[0]["id"]
        actor_id = bundle_objects[1]["id"]
        bundle_objects.append(build_relationship(source_ref=indicator_id, target_ref=actor_id, relationship_type="indicates"))

    bundle = {
        "type": "bundle",
        "id": _make_id("bundle"),
        "spec_version": "2.1",
        "objects": list(bundle_objects),
    }
    return bundle


def create_stix_bundle(*args: Any, **kwargs: Any) -> dict[str, Any]:
    return build_stix_bundle(*args, **kwargs)


def export_stix_bundle(*args: Any, **kwargs: Any) -> dict[str, Any]:
    return build_stix_bundle(*args, **kwargs)


def generate_verislip_threat_bundle(*args: Any, **kwargs: Any) -> dict[str, Any]:
    return build_stix_bundle(*args, **kwargs)


def get_default_verislip_bundle() -> dict[str, Any]:
    return build_stix_bundle()


__all__ = [
    "build_indicator",
    "build_observed_data",
    "build_relationship",
    "build_stix_bundle",
    "create_stix_bundle",
    "export_stix_bundle",
    "generate_verislip_threat_bundle",
    "get_default_verislip_bundle",
]
