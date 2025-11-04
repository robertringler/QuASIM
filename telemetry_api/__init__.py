"""Telemetry API adapters for SpaceX and NASA data ingestion.

This module provides JSON-RPC and gRPC adapters for ingesting telemetry data
from SpaceX (Falcon 9 ascent, engine, attitude, GNC loops), NASA (Orion/SLS
GNC data), Dragon spacecraft (trajectory and GNC), and Starship vehicle
(dynamics and GNC scenarios) into QuASIM's simulation pipeline.
"""

from __future__ import annotations

from .dragon_adapter import DragonTelemetryAdapter, DragonTelemetrySchema
from .nasa_adapter import NASATelemetryAdapter, NASATelemetrySchema
from .spacex_adapter import SpaceXTelemetryAdapter, SpaceXTelemetrySchema
from .starship_adapter import StarshipTelemetryAdapter, StarshipTelemetrySchema

__all__ = [
    "SpaceXTelemetryAdapter",
    "SpaceXTelemetrySchema",
    "NASATelemetryAdapter",
    "NASATelemetrySchema",
    "DragonTelemetryAdapter",
    "DragonTelemetrySchema",
    "StarshipTelemetryAdapter",
    "StarshipTelemetrySchema",
]
