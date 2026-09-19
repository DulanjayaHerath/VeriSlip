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

    def _escape_label_value(value: str) -> str:
        return str(value).replace("\\", "\\\\").replace("\n", "\\n").replace('"', '\\"')

    class _FallbackRegistry:
        def __init__(self):
            self._metrics = []

        def register(self, metric):
            self._metrics.append(metric)
            return metric

        def collect(self):
            return list(self._metrics)

    class _FallbackSample:
        def __init__(self, metric, labels):
            self.metric = metric
            self.labels = labels
            self.value = 0.0
            self.observed_values = []

        def inc(self, amount: float = 1.0):
            self.value += float(amount)

        def observe(self, amount: float):
            self.observed_values.append(float(amount))

        def set(self, value: float):
            self.value = float(value)

    class _BaseFallbackMetric:
        def __init__(self, name: str, documentation: str, labelnames=(), buckets=None):
            self.name = name
            self.documentation = documentation
            self.labelnames = list(labelnames)
            self.buckets = tuple(float(bucket) for bucket in (buckets or ()))
            self._samples = {}
            REGISTRY.register(self)

        def _resolve_labels(self, args, kwargs):
            if not self.labelnames:
                if args or kwargs:
                    raise ValueError(f"{self.name} does not expect label values")
                return {}

            if args and kwargs:
                raise ValueError(f"{self.name} cannot accept positional and keyword labels together")

            if args:
                if len(args) != len(self.labelnames):
                    raise ValueError(f"{self.name} expects {len(self.labelnames)} label values")
                label_values = dict(zip(self.labelnames, args))
            else:
                label_values = dict(kwargs)
                missing = [name for name in self.labelnames if name not in label_values]
                extra = [name for name in label_values if name not in self.labelnames]
                if missing or extra:
                    raise ValueError(f"{self.name} labels mismatch: missing={missing}, extra={extra}")

            return label_values

        def _default_sample(self):
            if () not in self._samples:
                self._samples[()] = _FallbackSample(self, {})
            return self._samples[()]

        def labels(self, *args, **kwargs):
            label_values = self._resolve_labels(args, kwargs)
            key = tuple(label_values.get(name) for name in self.labelnames)
            if key not in self._samples:
                self._samples[key] = _FallbackSample(self, label_values)
            return self._samples[key]

        def inc(self, amount: float = 1.0, *args, **kwargs):
            sample = self.labels(*args, **kwargs) if self.labelnames else self._default_sample()
            sample.inc(amount)

        def observe(self, amount: float, *args, **kwargs):
            sample = self.labels(*args, **kwargs) if self.labelnames else self._default_sample()
            sample.observe(amount)

        def set(self, value: float, *args, **kwargs):
            sample = self.labels(*args, **kwargs) if self.labelnames else self._default_sample()
            sample.set(value)

        def _format_labels(self, label_values):
            if not label_values:
                return ""
            return "{" + ",".join(
                f'{name}="{_escape_label_value(str(value))}"' for name, value in label_values.items()
            ) + "}"

        def render(self):
            raise NotImplementedError

    class _FallbackCounter(_BaseFallbackMetric):
        def render(self):
            lines = [
                f"# HELP {self.name} {self.documentation}",
                f"# TYPE {self.name} counter",
            ]
            for sample in self._samples.values():
                lines.append(f"{self.name}{self._format_labels(sample.labels)} {sample.value}")
            return "\n".join(lines)

    class _FallbackHistogram(_BaseFallbackMetric):
        def render(self):
            lines = [
                f"# HELP {self.name} {self.documentation}",
                f"# TYPE {self.name} histogram",
            ]
            ordered_buckets = list(self.buckets) + [float("inf")]
            for sample in self._samples.values():
                label_values = dict(sample.labels)
                total_count = len(sample.observed_values)
                total_sum = sum(sample.observed_values)
                for bucket in ordered_buckets:
                    bucket_labels = dict(label_values)
                    bucket_labels["le"] = "+Inf" if bucket == float("inf") else str(bucket)
                    count = sum(1 for value in sample.observed_values if value <= bucket)
                    lines.append(f"{self.name}_bucket{self._format_labels(bucket_labels)} {count}")
                lines.append(f"{self.name}_sum{self._format_labels(label_values)} {total_sum}")
                lines.append(f"{self.name}_count{self._format_labels(label_values)} {total_count}")
            return "\n".join(lines)

    class _FallbackGauge(_BaseFallbackMetric):
        def render(self):
            lines = [
                f"# HELP {self.name} {self.documentation}",
                f"# TYPE {self.name} gauge",
            ]
            for sample in self._samples.values():
                lines.append(f"{self.name}{self._format_labels(sample.labels)} {sample.value}")
            return "\n".join(lines)

    REGISTRY = _FallbackRegistry()

    class Counter(_FallbackCounter):
        def __init__(self, name: str, documentation: str, labelnames=(), **kwargs):
            labels = labelnames or kwargs.get("label_names", ())
            super().__init__(name, documentation, labels)

    class Histogram(_FallbackHistogram):
        def __init__(self, name: str, documentation: str, labelnames=(), buckets=None, **kwargs):
            labels = labelnames or kwargs.get("label_names", ())
            b = buckets if buckets is not None else kwargs.get("buckets")
            super().__init__(name, documentation, labels, b)

    class Gauge(_FallbackGauge):
        def __init__(self, name: str, documentation: str, labelnames=(), **kwargs):
            labels = labelnames or kwargs.get("label_names", ())
            super().__init__(name, documentation, labels)

    def generate_latest(registry=None) -> bytes:
        metrics = registry.collect() if registry is not None else REGISTRY.collect()
        lines = []
        for metric in metrics:
            rendered = metric.render()
            if rendered:
                lines.append(rendered)
        payload = "\n".join(lines)
        if payload:
            payload += "\n"
        return payload.encode("utf-8")

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
