"""Telemetry API adapters for SpaceX and NASA data ingestion.

This module provides JSON-RPC and gRPC adapters for ingesting telemetry data
from SpaceX (Falcon 9 ascent, engine, attitude, GNC loops) and NASA (Orion/SLS
GNC data) into QuASIM's simulation pipeline.
"""

from __future__ import annotations

from .nasa_adapter import NASATelemetryAdapter, NASATelemetrySchema
from .spacex_adapter import SpaceXTelemetryAdapter, SpaceXTelemetrySchema

__all__ = [
    "SpaceXTelemetryAdapter",
    "SpaceXTelemetrySchema",
    "NASATelemetryAdapter",
    "NASATelemetrySchema",
]
