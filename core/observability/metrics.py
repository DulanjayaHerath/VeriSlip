"""
Observability Subsystem: Prometheus Metrics for VeriSlip API & Forensic Engine (#88).
Monitors:
- Request latencies & throughput
- Per-layer execution times (Layer 1, Layer 2, Layer 3, Layer 4)
- Verification verdict distributions
- Active learning queue size
"""

import time
from typing import Dict, Any, Optional

try:
    from prometheus_client import (
        Counter,
        Histogram,
        Gauge,
        generate_latest,
        CONTENT_TYPE_LATEST,
        REGISTRY
    )
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False
    CONTENT_TYPE_LATEST = "text/plain; version=0.0.4; charset=utf-8"

    def _format_labels(labels):
        if not labels:
            return ""
        return "{" + ",".join(f'{key}="{value}"' for key, value in labels.items()) + "}"

    class _BoundMetric:
        def __init__(self, metric, labels):
            self.metric = metric
            self.labels_map = labels or {}

        def inc(self, amount: float = 1.0, **kwargs):
            self.metric._inc(self.labels_map, amount)

        def observe(self, amount: float, **kwargs):
            self.metric._observe(self.labels_map, amount)

        def set(self, value: float, **kwargs):
            self.metric._set(self.labels_map, value)

    class _FallbackMetric:
        def __init__(self, name, documentation, label_names=(), metric_type="counter", buckets=None):
            self.name = name
            self.documentation = documentation
            self.label_names = list(label_names)
            self.metric_type = metric_type
            self.buckets = list(buckets or [])
            self._values = {}
            self._histograms = {}
            self._registered = False

        def inc(self, amount: float = 1.0, **kwargs):
            self._inc({}, amount)

        def observe(self, amount: float, **kwargs):
            self._observe({}, amount)

        def set(self, value: float, **kwargs):
            self._set({}, value)

        def labels(self, *args, **kwargs):
            if args:
                raise TypeError("Positional labels are not supported in fallback metrics.")
            ordered = {key: kwargs.get(key, "") for key in self.label_names}
            return _BoundMetric(self, ordered)

        def _label_key(self, labels):
            ordered = tuple(str(labels.get(key, "")) for key in self.label_names)
            return ordered

        def _set(self, labels, value):
            self._values[self._label_key(labels)] = float(value)

        def _inc(self, labels, value):
            key = self._label_key(labels)
            self._values[key] = float(self._values.get(key, 0.0)) + float(value)

        def _observe(self, labels, value):
            value = float(value)
            key = self._label_key(labels)
            metric = self._histograms.setdefault(key, {"count": 0.0, "sum": 0.0, "buckets": {}})
            metric["count"] += 1.0
            metric["sum"] += value
            for upper_bound in self.buckets:
                if value <= upper_bound:
                    metric["buckets"][upper_bound] = metric["buckets"].get(upper_bound, 0.0) + 1.0
            metric["buckets"][float("inf")] = metric["buckets"].get(float("inf"), 0.0) + 1.0

        def collect(self):
            return self

        def render(self):
            lines = [
                f"# HELP {self.name} {self.documentation}",
                f"# TYPE {self.name} {self.metric_type}",
            ]
            if self.metric_type == "histogram":
                for labels, metric in sorted(self._histograms.items()):
                    label_str = _format_labels(dict(zip(self.label_names, labels)))
                    cumulative = 0.0
                    for upper_bound in self.buckets:
                        cumulative += metric["buckets"].get(upper_bound, 0.0)
                        bucket_labels = dict(zip(self.label_names, labels))
                        bucket_labels["le"] = str(upper_bound)
                        lines.append(f"{self.name}_bucket{_format_labels(bucket_labels)} {cumulative}")
                    bucket_labels = dict(zip(self.label_names, labels))
                    bucket_labels["le"] = "+Inf"
                    lines.append(f"{self.name}_bucket{_format_labels(bucket_labels)} {metric['count']}")
                    lines.append(f"{self.name}_sum{label_str} {metric['sum']}")
                    lines.append(f"{self.name}_count{label_str} {metric['count']}")
            else:
                for labels, value in sorted(self._values.items()):
                    label_str = _format_labels(dict(zip(self.label_names, labels)))
                    lines.append(f"{self.name}{label_str} {value}")
            return lines

    class _FallbackRegistry:
        def __init__(self):
            self._metrics = []

        def register(self, metric):
            self._metrics.append(metric)
            return metric

        def collect(self):
            return list(self._metrics)

    class Counter(_FallbackMetric):
        def __init__(self, name, documentation, label_names=None, **kwargs):
            super().__init__(name, documentation, label_names or (), "counter")
            REGISTRY.register(self)

    class Gauge(_FallbackMetric):
        def __init__(self, name, documentation, label_names=None, **kwargs):
            super().__init__(name, documentation, label_names or (), "gauge")
            REGISTRY.register(self)

    class Histogram(_FallbackMetric):
        def __init__(self, name, documentation, label_names=None, buckets=None, **kwargs):
            super().__init__(name, documentation, label_names or (), "histogram", buckets or [])
            REGISTRY.register(self)

    REGISTRY = _FallbackRegistry()

    def generate_latest(registry=None) -> bytes:
        metrics = registry.collect() if registry is not None else REGISTRY.collect()
        output = []
        for metric in metrics:
            output.extend(metric.render())
        return ("\n".join(output) + "\n").encode("utf-8")

# HTTP Request Metrics
HTTP_REQUESTS_TOTAL = Counter(
    "verislip_http_requests_total",
    "Total HTTP requests received by VeriSlip API",
    ["method", "endpoint", "status_code"]
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "verislip_http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0]
)

# Forensic Layer Timing Breakdown
FORENSIC_LAYER_DURATION_SECONDS = Histogram(
    "verislip_forensic_layer_duration_seconds",
    "Latency per forensic analysis layer in seconds",
    ["layer_name"],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.2, 0.5, 1.0]
)

# Domain Metrics
VERIFICATION_VERDICTS_TOTAL = Counter(
    "verislip_verification_verdicts_total",
    "Total transaction slip verification verdicts generated",
    ["verdict", "bank_name"]
)

ACTIVE_LEARNING_QUEUE_SIZE = Gauge(
    "verislip_active_learning_queue_size",
    "Number of ambiguous slips currently queued for expert human triage"
)


def record_request_metrics(method: str, endpoint: str, status_code: int, duration_seconds: float):
    """Record incoming HTTP request throughput and latency."""
    HTTP_REQUESTS_TOTAL.labels(method=method, endpoint=endpoint, status_code=str(status_code)).inc()
    HTTP_REQUEST_DURATION_SECONDS.labels(method=method, endpoint=endpoint).observe(duration_seconds)


def record_layer_duration(layer_name: str, duration_seconds: float):
    """Record execution latency for an individual forensic layer."""
    FORENSIC_LAYER_DURATION_SECONDS.labels(layer_name=layer_name).observe(duration_seconds)


def record_verification_verdict(verdict: str, bank_name: Optional[str] = None):
    """Record generated verdict and identified issuing bank."""
    bank = bank_name or "UNKNOWN"
    VERIFICATION_VERDICTS_TOTAL.labels(verdict=verdict, bank_name=bank).inc()


def set_active_learning_queue_gauge(count: int):
    """Update active learning queue depth gauge."""
    ACTIVE_LEARNING_QUEUE_SIZE.set(count)


def get_metrics_payload() -> bytes:
    """Generate latest Prometheus exposition payload."""
    return generate_latest(REGISTRY)
