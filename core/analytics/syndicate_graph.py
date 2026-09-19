"""Graph-based fraud syndicate detection utilities.

This module intentionally avoids strict PyTorch/torch_geometric requirements so the
project keeps working in lightweight environments while still exposing the graph
structure needed for syndicate-risk analysis.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Sequence


DEFAULT_ENTITY_TYPES = ("merchant", "account", "device", "hash", "transaction")


@dataclass(frozen=True)
class GraphNode:
    node_id: str
    node_type: str
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload = {"id": self.node_id, "type": self.node_type}
        payload.update(self.attributes)
        return payload


@dataclass(frozen=True)
class GraphEdge:
    source: str
    target: str
    relation: str
    weight: float = 1.0
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "target": self.target,
            "relation": self.relation,
            "weight": self.weight,
            **self.attributes,
        }


@dataclass
class FraudRingCluster:
    members: List[str]
    merchant_ids: List[str]
    account_ids: List[str]
    perceptual_hashes: List[str]
    transaction_ids: List[str]
    shared_account_count: int = 0
    shared_hash_count: int = 0
    cluster_score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "members": self.members,
            "merchant_ids": self.merchant_ids,
            "account_ids": self.account_ids,
            "perceptual_hashes": self.perceptual_hashes,
            "transaction_ids": self.transaction_ids,
            "shared_account_count": self.shared_account_count,
            "shared_hash_count": self.shared_hash_count,
            "cluster_score": round(self.cluster_score, 4),
        }


class SyndicateGraph:
    """Container representing a heterogeneous fraud graph."""

    def __init__(self, nodes: Optional[Iterable[GraphNode]] = None, edges: Optional[Iterable[GraphEdge]] = None):
        self.nodes = list(nodes or [])
        self.edges = list(edges or [])
        self.node_index = {node.node_id: node for node in self.nodes}
        self.adjacency: Dict[str, List[GraphEdge]] = defaultdict(list)
        for edge in self.edges:
            self.adjacency[edge.source].append(edge)
            self.adjacency[edge.target].append(edge)

    @classmethod
    def from_transactions(cls, transactions: Sequence[Dict[str, Any]]) -> "SyndicateGraph":
        builder = SyndicateGraphBuilder()
        return builder.build(transactions)

    def add_transaction(self, transaction: Dict[str, Any]) -> None:
        builder = SyndicateGraphBuilder()
        built = builder.build([transaction])
        self.nodes.extend(built.nodes)
        self.edges.extend(built.edges)
        self.node_index.update(built.node_index)
        for edge in built.edges:
            self.adjacency[edge.source].append(edge)
            self.adjacency[edge.target].append(edge)

    def find_clusters(self, min_cluster_size: int = 2) -> List[FraudRingCluster]:
        visited: set[str] = set()
        components: List[List[str]] = []

        for node in self.node_index:
            if node in visited:
                continue

            stack = [node]
            component: List[str] = []
            visited.add(node)
            while stack:
                current = stack.pop()
                component.append(current)
                for edge in self.adjacency.get(current, []):
                    neighbor = edge.target if edge.source == current else edge.source
                    if neighbor not in visited:
                        visited.add(neighbor)
                        stack.append(neighbor)

            if len(component) >= min_cluster_size:
                components.append(sorted(component))

        clusters: List[FraudRingCluster] = []
        for component in components:
            merchant_ids = sorted({self.node_index[nid].node_id for nid in component if self.node_index[nid].node_type == "merchant"})
            account_ids = sorted({self.node_index[nid].node_id for nid in component if self.node_index[nid].node_type == "account"})
            perceptual_hashes = sorted({self.node_index[nid].node_id for nid in component if self.node_index[nid].node_type == "hash"})
            transaction_ids = sorted({self.node_index[nid].node_id for nid in component if self.node_index[nid].node_type == "transaction"})

            repeated_account_count = 0
            repeated_hash_count = 0
            account_usage: Dict[str, set[str]] = defaultdict(set)
            hash_usage: Dict[str, set[str]] = defaultdict(set)
            for edge in self.edges:
                if edge.source in component and edge.target in component:
                    source_node = self.node_index.get(edge.source)
                    target_node = self.node_index.get(edge.target)
                    if source_node and target_node:
                        if source_node.node_type == "transaction" and target_node.node_type == "account":
                            account_usage[target_node.node_id].add(source_node.attributes.get("merchant_id", ""))
                        elif source_node.node_type == "account" and target_node.node_type == "transaction":
                            account_usage[source_node.node_id].add(target_node.attributes.get("merchant_id", ""))
                        if source_node.node_type == "transaction" and target_node.node_type == "hash":
                            hash_usage[target_node.node_id].add(source_node.attributes.get("merchant_id", ""))
                        elif source_node.node_type == "hash" and target_node.node_type == "transaction":
                            hash_usage[source_node.node_id].add(target_node.attributes.get("merchant_id", ""))

            repeated_account_count = sum(1 for account_id, merchants in account_usage.items() if len(merchants) > 1)
            repeated_hash_count = sum(1 for hash_id, merchants in hash_usage.items() if len(merchants) > 1)

            cluster_score = 0.0
            if len(merchant_ids) >= 2:
                cluster_score += 0.25
            if repeated_account_count:
                cluster_score += min(0.4, repeated_account_count / max(1, len(merchant_ids)) * 0.4)
            if repeated_hash_count:
                cluster_score += min(0.4, repeated_hash_count / max(1, len(merchant_ids)) * 0.5)
            cluster_score += min(0.2, len(transaction_ids) / 20.0)
            cluster_score = max(0.0, min(1.0, cluster_score))

            clusters.append(
                FraudRingCluster(
                    members=component,
                    merchant_ids=merchant_ids,
                    account_ids=account_ids,
                    perceptual_hashes=perceptual_hashes,
                    transaction_ids=transaction_ids,
                    shared_account_count=repeated_account_count,
                    shared_hash_count=repeated_hash_count,
                    cluster_score=cluster_score,
                )
            )

        return sorted(clusters, key=lambda item: item.cluster_score, reverse=True)

    def compute_syndicate_risk(self, min_cluster_size: int = 2) -> float:
        clusters = self.find_clusters(min_cluster_size=min_cluster_size)
        if not clusters:
            return 0.0
        weights = [cluster.cluster_score for cluster in clusters]
        return round(sum(weights) / max(1, len(weights)), 4)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_count": len(self.nodes),
            "edge_count": len(self.edges),
            "nodes": [node.to_dict() for node in self.nodes],
            "edges": [edge.to_dict() for edge in self.edges],
        }


class SyndicateGraphBuilder:
    """Builds a heterogeneous graph from transaction-like records."""

    def __init__(self, default_entity_types: Sequence[str] = DEFAULT_ENTITY_TYPES):
        self.default_entity_types = tuple(default_entity_types)

    def _normalize_transaction(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        normalized = dict(transaction)
        normalized.setdefault("transaction_id", normalized.get("id", "tx_0000"))
        normalized.setdefault("merchant_id", normalized.get("merchant", "MERCHANT_UNKNOWN"))
        normalized.setdefault("account_id", normalized.get("account", "ACCOUNT_UNKNOWN"))
        normalized.setdefault("device_fingerprint", normalized.get("device", "DEVICE_UNKNOWN"))
        normalized.setdefault("perceptual_hash", normalized.get("hash", normalized.get("p_hash", "HASH_UNKNOWN")))
        normalized.setdefault("amount_lkr", normalized.get("amount", 0.0))
        return normalized

    def build(self, transactions: Sequence[Dict[str, Any]]) -> SyndicateGraph:
        nodes: List[GraphNode] = []
        edges: List[GraphEdge] = []
        seen_nodes: set[str] = set()

        for raw_transaction in transactions:
            tx = self._normalize_transaction(raw_transaction)
            merchant_id = str(tx["merchant_id"])
            account_id = str(tx["account_id"])
            device_id = str(tx["device_fingerprint"])
            hash_id = str(tx["perceptual_hash"])
            transaction_id = str(tx["transaction_id"])

            def add_node(node_id: str, node_type: str, **attrs):
                if node_id not in seen_nodes:
                    nodes.append(GraphNode(node_id=node_id, node_type=node_type, attributes=attrs))
                    seen_nodes.add(node_id)
                elif node_type in {"merchant", "account", "device", "hash", "transaction"}:
                    for node in nodes:
                        if node.node_id == node_id and node.node_type == node_type:
                            for key, value in attrs.items():
                                node.attributes[key] = value
                            break

            add_node(f"M:{merchant_id}", "merchant", merchant_id=merchant_id)
            add_node(f"A:{account_id}", "account", account_id=account_id)
            add_node(f"D:{device_id}", "device", device_id=device_id)
            add_node(f"H:{hash_id}", "hash", perceptual_hash=hash_id)
            add_node(f"T:{transaction_id}", "transaction", merchant_id=merchant_id, account_id=account_id, device_id=device_id, perceptual_hash=hash_id, amount_lkr=tx.get("amount_lkr"))

            edges.extend(
                [
                    GraphEdge(f"T:{transaction_id}", f"M:{merchant_id}", "ORDERED_AT", weight=1.0, attributes={"merchant_id": merchant_id}),
                    GraphEdge(f"T:{transaction_id}", f"A:{account_id}", "TRANSFERRED_TO", weight=1.0, attributes={"account_id": account_id}),
                    GraphEdge(f"T:{transaction_id}", f"D:{device_id}", "ORIGINATED_FROM", weight=1.0, attributes={"device_id": device_id}),
                    GraphEdge(f"T:{transaction_id}", f"H:{hash_id}", "HAS_IMAGE", weight=1.0, attributes={"perceptual_hash": hash_id}),
                ]
            )

        return SyndicateGraph(nodes=nodes, edges=edges)

    def build_synthetic_ring(self, merchant_count: int = 5) -> SyndicateGraph:
        shared_account = "ACC_SHARED_9381"
        shared_hash = "PHASH_5F3E72C9"
        base_transactions: List[Dict[str, Any]] = []

        for index in range(merchant_count):
            merchant_id = f"M{index + 1}"
            for invoice_index in range(3):
                transaction_id = f"TXN-{merchant_id}-{invoice_index + 1}"
                base_transactions.append(
                    {
                        "transaction_id": transaction_id,
                        "merchant_id": merchant_id,
                        "account_id": shared_account,
                        "device_fingerprint": f"DEV-{(index + 1) * 10 + invoice_index}",
                        "perceptual_hash": shared_hash,
                        "amount_lkr": 15000.0 + (index * 500) + invoice_index * 250,
                    }
                )

        return self.build(base_transactions)

    def build_api_payload(self, transactions: Optional[Sequence[Dict[str, Any]]] = None) -> Dict[str, Any]:
        graph = self.build(transactions or [])
        clusters = graph.find_clusters(min_cluster_size=2)
        risk_index = graph.compute_syndicate_risk(min_cluster_size=2)
        return {
            "status": "operational",
            "timestamp": 0,
            "syndicate_risk_index": round(risk_index, 4),
            "risk_level": self._risk_level(risk_index),
            "graph_summary": {
                "node_count": len(graph.nodes),
                "edge_count": len(graph.edges),
                "merchant_count": sum(1 for node in graph.nodes if node.node_type == "merchant"),
                "account_count": sum(1 for node in graph.nodes if node.node_type == "account"),
                "hash_count": sum(1 for node in graph.nodes if node.node_type == "hash"),
                "transaction_count": sum(1 for node in graph.nodes if node.node_type == "transaction"),
            },
            "clusters": [cluster.to_dict() for cluster in clusters],
            "graph": graph.to_dict(),
        }

    @staticmethod
    def _risk_level(risk_index: float) -> str:
        if risk_index >= 0.8:
            return "CRITICAL"
        if risk_index >= 0.6:
            return "HIGH"
        if risk_index >= 0.3:
            return "MEDIUM"
        return "LOW"


def simulate_syndicate_ring(merchant_count: int = 5) -> Dict[str, Any]:
    """Convenience wrapper used by scripts and API endpoints."""
    builder = SyndicateGraphBuilder()
    graph = builder.build_synthetic_ring(merchant_count=merchant_count)
    clusters = graph.find_clusters(min_cluster_size=2)
    payload = {
        "status": "operational",
        "graph_summary": {
            "node_count": len(graph.nodes),
            "edge_count": len(graph.edges),
            "merchant_count": sum(1 for node in graph.nodes if node.node_type == "merchant"),
            "account_count": sum(1 for node in graph.nodes if node.node_type == "account"),
            "hash_count": sum(1 for node in graph.nodes if node.node_type == "hash"),
            "transaction_count": sum(1 for node in graph.nodes if node.node_type == "transaction"),
        },
        "syndicate_risk_index": graph.compute_syndicate_risk(min_cluster_size=2),
        "risk_level": SyndicateGraphBuilder._risk_level(graph.compute_syndicate_risk(min_cluster_size=2)),
        "clusters": [cluster.to_dict() for cluster in clusters],
    }
    return payload
