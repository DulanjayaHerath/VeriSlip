#!/usr/bin/env python3
"""Simulate a five-merchant fraud syndicate ring and print the graph risk."""

from __future__ import annotations

import json

from core.analytics.syndicate_graph import simulate_syndicate_ring


if __name__ == "__main__":
    payload = simulate_syndicate_ring(merchant_count=5)
    print(json.dumps(payload, indent=2, sort_keys=True))
