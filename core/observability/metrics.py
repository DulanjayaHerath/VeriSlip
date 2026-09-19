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
    REGISTRY = None

    class _MockMetric:
        def __init__(self, *args, **kwargs):
            pass

        def labels(self, *args, **kwargs):
            return self

        def inc(self, *args, **kwargs):
            pass

        def observe(self, *args, **kwargs):
            pass

        def set(self, *args, **kwargs):
            pass

    Counter = _MockMetric
    Histogram = _MockMetric
    Gauge = _MockMetric

    def generate_latest(registry=None) -> bytes:
        return b"# VeriSlip fallback metrics (prometheus_client not installed)\n"

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
