"""Append-only Merkle audit ledger for forensic verification evidence."""

from __future__ import annotations

import hashlib
import json
import re
import threading
from dataclasses import dataclass
from typing import Any, Mapping, Sequence


_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def _canonical_json(value: Mapping[str, Any]) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def _hash_leaf(payload: Mapping[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(payload)).hexdigest()


def _hash_pair(left: str, right: str) -> str:
    return hashlib.sha256(bytes.fromhex(left) + bytes.fromhex(right)).hexdigest()


@dataclass(frozen=True)
class AuditReceipt:
    """A self-contained proof that one audit entry belongs to a Merkle root."""

    index: int
    leaf_hash: str
    root: str
    siblings: tuple[dict[str, str], ...]
    entry: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "index": self.index,
            "leaf_hash": self.leaf_hash,
            "root": self.root,
            "siblings": list(self.siblings),
            "entry": self.entry,
        }


class MerkleAuditLedger:
    """In-memory append-only ledger with SHA-256 Merkle inclusion proofs.

    Entries are never edited or removed. The optional ``entries`` argument is
    intended for restoring a previously persisted append-only log.
    """

    def __init__(self, entries: Sequence[Mapping[str, Any]] | None = None) -> None:
        self._lock = threading.RLock()
        self._entries: list[dict[str, Any]] = []
        self._leaf_hashes: list[str] = []
        for entry in entries or ():
            self._append_restored(entry)

    @staticmethod
    def _validate_slip_hash(slip_sha256: str) -> str:
        if not isinstance(slip_sha256, str) or not _SHA256_RE.fullmatch(slip_sha256):
            raise ValueError("slip_sha256 must be a 64-character hexadecimal SHA-256 digest")
        return slip_sha256.lower()

    def _append_restored(self, entry: Mapping[str, Any]) -> None:
        required = {"slip_sha256", "timestamp", "layer_scores", "verdict", "bounding_boxes", "merchant_signature"}
        if set(entry) < required:
            raise ValueError("restored audit entry is missing required fields")
        normalized = {
            "slip_sha256": self._validate_slip_hash(entry["slip_sha256"]),
            "timestamp": str(entry["timestamp"]),
            "layer_scores": entry["layer_scores"],
            "verdict": str(entry["verdict"]),
            "bounding_boxes": entry["bounding_boxes"],
            "merchant_signature": entry["merchant_signature"],
        }
        self._entries.append(normalized)
        self._leaf_hashes.append(_hash_leaf(normalized))

    @property
    def size(self) -> int:
        with self._lock:
            return len(self._entries)

    @property
    def root(self) -> str | None:
        with self._lock:
            return self._root_for(self._leaf_hashes)

    def append(
        self,
        *,
        slip_sha256: str,
        timestamp: str,
        layer_scores: Mapping[str, Any],
        verdict: str,
        bounding_boxes: Sequence[Any] = (),
        merchant_signature: str | None = None,
    ) -> AuditReceipt:
        """Append one forensic event and return its current inclusion proof."""
        entry = {
            "slip_sha256": self._validate_slip_hash(slip_sha256),
            "timestamp": str(timestamp),
            "layer_scores": dict(layer_scores),
            "verdict": str(verdict),
            "bounding_boxes": list(bounding_boxes),
            "merchant_signature": merchant_signature,
        }
        with self._lock:
            index = len(self._entries)
            self._entries.append(entry)
            self._leaf_hashes.append(_hash_leaf(entry))
            return self._receipt_for(index)

    @staticmethod
    def _root_for(leaves: Sequence[str]) -> str | None:
        if not leaves:
            return None
        level = list(leaves)
        while len(level) > 1:
            level = [
                _hash_pair(level[i], level[i + 1 if i + 1 < len(level) else i])
                for i in range(0, len(level), 2)
            ]
        return level[0]

    def _receipt_for(self, index: int) -> AuditReceipt:
        level = list(self._leaf_hashes)
        position = index
        siblings: list[dict[str, str]] = []
        while len(level) > 1:
            sibling_index = position - 1 if position % 2 else position + 1
            if sibling_index >= len(level):
                sibling_index = position
            siblings.append({
                "side": "left" if position % 2 else "right",
                "hash": level[sibling_index],
            })
            level = [
                _hash_pair(level[i], level[i + 1 if i + 1 < len(level) else i])
                for i in range(0, len(level), 2)
            ]
            position //= 2
        return AuditReceipt(
            index=index,
            leaf_hash=self._leaf_hashes[index],
            root=level[0],
            siblings=tuple(siblings),
            entry=dict(self._entries[index]),
        )

    @staticmethod
    def verify_proof(receipt: AuditReceipt | Mapping[str, Any]) -> bool:
        """Verify both the entry hash and its path to the claimed root."""
        data = receipt.to_dict() if isinstance(receipt, AuditReceipt) else receipt
        try:
            entry = data["entry"]
            current = _hash_leaf(entry)
            if current != data["leaf_hash"]:
                return False
            for sibling in data["siblings"]:
                if sibling["side"] == "left":
                    current = _hash_pair(sibling["hash"], current)
                elif sibling["side"] == "right":
                    current = _hash_pair(current, sibling["hash"])
                else:
                    return False
            return current == data["root"]
        except (KeyError, TypeError, ValueError):
            return False
