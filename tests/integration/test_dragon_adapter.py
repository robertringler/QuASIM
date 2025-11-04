"""Integration tests for Dragon spacecraft telemetry adapter."""

from __future__ import annotations

import pytest

from telemetry_api import DragonTelemetryAdapter, DragonTelemetrySchema


class TestDragonTelemetryAdapter:
    """Test suite for Dragon telemetry adapter."""

    def test_adapter_initialization(self):
        """Test adapter initializes with correct defaults."""
        adapter = DragonTelemetryAdapter()
        assert adapter.endpoint == "localhost:8002"
        assert not adapter._connected
        assert adapter._schema_version == "1.0"

    def test_adapter_connection(self):
        """Test adapter connection functionality."""
        adapter = DragonTelemetryAdapter()
        assert adapter.connect()
        assert adapter._connected

        adapter.disconnect()
        assert not adapter._connected

    def test_parse_minimal_telemetry(self):
        """Test parsing minimal valid telemetry data."""
        adapter = DragonTelemetryAdapter()
        raw_data = {
            "timestamp": 100.5,
            "vehicle_id": "Dragon_C210",
        }

        telemetry = adapter.parse_telemetry(raw_data)

        assert telemetry.timestamp == 100.5
        assert telemetry.vehicle_id == "Dragon_C210"
        assert isinstance(telemetry.trajectory_data, dict)
        assert isinstance(telemetry.thermal_data, dict)
        assert isinstance(telemetry.power_data, dict)
        assert isinstance(telemetry.gnc_data, dict)
        assert isinstance(telemetry.docking_data, dict)

    def test_parse_full_telemetry(self):
        """Test parsing comprehensive telemetry data."""
        adapter = DragonTelemetryAdapter()
        raw_data = {
            "timestamp": 250.0,
            "vehicle_id": "Dragon_C210",
            "position": [6_700_000.0, 0.0, 0.0],
            "velocity": [0.0, 7500.0, 0.0],
            "acceleration": [0.0, 0.0, 0.0],
            "altitude": 400_000.0,
            "orbital_phase": "LEO",
            "attitude_q": [0.7071, 0.7071, 0.0, 0.0],
            "angular_vel": [0.01, 0.0, 0.0],
            "control_mode": "NOMINAL",
            "rcs_propellant": 95.5,
            "radiator_temp": 10.0,
            "cabin_temp": 22.0,
            "battery_temp": 25.0,
            "thermal_mode": "NOMINAL",
            "solar_voltage": 120.0,
            "battery_soc": 98.0,
            "power_draw": 2500.0,
            "charging": True,
            "docking_status": "APPROACH",
            "rel_range": 100.0,
            "rel_velocity": 0.1,
            "align_error": 0.5,
        }

        telemetry = adapter.parse_telemetry(raw_data)

        assert telemetry.timestamp == 250.0
        assert telemetry.vehicle_id == "Dragon_C210"
        assert telemetry.trajectory_data["position_eci"] == [6_700_000.0, 0.0, 0.0]
        assert telemetry.trajectory_data["velocity_eci"] == [0.0, 7500.0, 0.0]
        assert telemetry.trajectory_data["altitude_m"] == 400_000.0
        assert telemetry.gnc_data["attitude_quaternion"] == [0.7071, 0.7071, 0.0, 0.0]
        assert telemetry.thermal_data["cabin_temp_c"] == 22.0
        assert telemetry.power_data["battery_soc_pct"] == 98.0
        assert telemetry.docking_data["docking_status"] == "APPROACH"

    def test_parse_missing_required_field(self):
        """Test parsing fails with missing required fields."""
        adapter = DragonTelemetryAdapter()

        # Missing vehicle_id
        raw_data = {"timestamp": 100.0}
        with pytest.raises(ValueError, match="Missing required field: vehicle_id"):
            adapter.parse_telemetry(raw_data)

        # Missing timestamp
        raw_data = {"vehicle_id": "Dragon_C210"}
        with pytest.raises(ValueError, match="Missing required field: timestamp"):
            adapter.parse_telemetry(raw_data)

    def test_validate_valid_telemetry(self):
        """Test validation passes for valid telemetry."""
        adapter = DragonTelemetryAdapter()
        telemetry = DragonTelemetrySchema(
            timestamp=100.0,
            vehicle_id="Dragon_C210",
            trajectory_data={
                "position_eci": [6_700_000.0, 0.0, 0.0],
                "velocity_eci": [0.0, 7500.0, 0.0],
            },
            gnc_data={
                "attitude_quaternion": [1.0, 0.0, 0.0, 0.0],
            },
            thermal_data={
                "cabin_temp_c": 22.0,
            },
            power_data={
                "battery_soc_pct": 95.0,
            },
            docking_data={
                "docking_status": "SEPARATED",
            },
        )

        is_valid, errors = adapter.validate_schema(telemetry)

        assert is_valid
        assert len(errors) == 0

    def test_validate_negative_timestamp(self):
        """Test validation fails for negative timestamp."""
        adapter = DragonTelemetryAdapter()
        telemetry = DragonTelemetrySchema(
            timestamp=-10.0,
            vehicle_id="Dragon_C210",
        )

        is_valid, errors = adapter.validate_schema(telemetry)

        assert not is_valid
        assert any("Timestamp must be non-negative" in err for err in errors)

    def test_validate_invalid_vehicle_id(self):
        """Test validation fails for invalid vehicle ID format."""
        adapter = DragonTelemetryAdapter()
        telemetry = DragonTelemetrySchema(
            timestamp=100.0,
            vehicle_id="Falcon9_B1067",
        )

        is_valid, errors = adapter.validate_schema(telemetry)

        assert not is_valid
        assert any("Invalid vehicle ID format" in err for err in errors)

    def test_validate_position_out_of_range(self):
        """Test validation fails for position out of orbital range."""
        adapter = DragonTelemetryAdapter()
        telemetry = DragonTelemetrySchema(
            timestamp=100.0,
            vehicle_id="Dragon_C210",
            trajectory_data={
                "position_eci": [100_000_000.0, 0.0, 0.0],  # Too far
                "velocity_eci": [0.0, 7500.0, 0.0],
            },
        )

        is_valid, errors = adapter.validate_schema(telemetry)

        assert not is_valid
        assert any("Position magnitude out of orbital range" in err for err in errors)

    def test_validate_velocity_out_of_range(self):
        """Test validation fails for excessive velocity."""
        adapter = DragonTelemetryAdapter()
        telemetry = DragonTelemetrySchema(
            timestamp=100.0,
            vehicle_id="Dragon_C210",
            trajectory_data={
                "position_eci": [6_700_000.0, 0.0, 0.0],
                "velocity_eci": [0.0, 20_000.0, 0.0],  # Too fast
            },
        )

        is_valid, errors = adapter.validate_schema(telemetry)

        assert not is_valid
        assert any("Velocity magnitude exceeds orbital" in err for err in errors)

    def test_validate_unnormalized_quaternion(self):
        """Test validation fails for unnormalized quaternion."""
        adapter = DragonTelemetryAdapter()
        telemetry = DragonTelemetrySchema(
            timestamp=100.0,
            vehicle_id="Dragon_C210",
            gnc_data={
                "attitude_quaternion": [1.0, 1.0, 0.0, 0.0],  # Not normalized
            },
        )

        is_valid, errors = adapter.validate_schema(telemetry)

        assert not is_valid
        assert any("Quaternion not normalized" in err for err in errors)

    def test_validate_cabin_temperature_out_of_range(self):
        """Test validation fails for cabin temperature out of safe range."""
        adapter = DragonTelemetryAdapter()
        telemetry = DragonTelemetrySchema(
            timestamp=100.0,
            vehicle_id="Dragon_C210",
            thermal_data={
                "cabin_temp_c": 100.0,  # Too hot
            },
        )

        is_valid, errors = adapter.validate_schema(telemetry)

        assert not is_valid
        assert any("Cabin temperature out of safe range" in err for err in errors)

    def test_validate_battery_soc_out_of_range(self):
        """Test validation fails for battery SOC out of range."""
        adapter = DragonTelemetryAdapter()
        telemetry = DragonTelemetrySchema(
            timestamp=100.0,
            vehicle_id="Dragon_C210",
            power_data={
                "battery_soc_pct": 150.0,  # Over 100%
            },
        )

        is_valid, errors = adapter.validate_schema(telemetry)

        assert not is_valid
        assert any("Battery SOC out of range" in err for err in errors)

    def test_validate_invalid_docking_status(self):
        """Test validation fails for invalid docking status."""
        adapter = DragonTelemetryAdapter()
        telemetry = DragonTelemetrySchema(
            timestamp=100.0,
            vehicle_id="Dragon_C210",
            docking_data={
                "docking_status": "INVALID",
            },
        )

        is_valid, errors = adapter.validate_schema(telemetry)

        assert not is_valid
        assert any("Invalid docking status" in err for err in errors)

    def test_ingest_batch_success(self):
        """Test batch ingestion with valid data."""
        adapter = DragonTelemetryAdapter()
        raw_batch = [
            {
                "timestamp": 100.0,
                "vehicle_id": "Dragon_C210",
                "position": [6_700_000.0, 0.0, 0.0],
                "velocity": [0.0, 7500.0, 0.0],
            },
            {
                "timestamp": 101.0,
                "vehicle_id": "Dragon_C210",
                "position": [6_700_000.0, 0.0, 0.0],
                "velocity": [0.0, 7500.0, 0.0],
            },
        ]

        successful, failed, errors = adapter.ingest_batch(raw_batch)

        assert successful == 2
        assert failed == 0
        assert len(errors) == 0

    def test_ingest_batch_with_failures(self):
        """Test batch ingestion with some invalid data."""
        adapter = DragonTelemetryAdapter()
        raw_batch = [
            {
                "timestamp": 100.0,
                "vehicle_id": "Dragon_C210",
            },
            {
                "timestamp": -50.0,  # Invalid negative timestamp
                "vehicle_id": "Dragon_C210",
            },
            {
                "vehicle_id": "Dragon_C210",  # Missing timestamp
            },
        ]

        successful, failed, errors = adapter.ingest_batch(raw_batch)

        assert successful == 1
        assert failed == 2
        assert len(errors) > 0

    def test_export_quasim_format(self):
        """Test export to QuASIM internal format."""
        adapter = DragonTelemetryAdapter()
        telemetry = DragonTelemetrySchema(
            timestamp=100.0,
            vehicle_id="Dragon_C210",
            trajectory_data={
                "position_eci": [6_700_000.0, 0.0, 0.0],
                "velocity_eci": [0.0, 7500.0, 0.0],
                "acceleration": [0.0, 0.0, 0.0],
                "altitude_m": 400_000.0,
                "orbital_phase": "LEO",
            },
            gnc_data={
                "attitude_quaternion": [1.0, 0.0, 0.0, 0.0],
                "angular_velocity": [0.0, 0.0, 0.0],
                "control_mode": "NOMINAL",
            },
            thermal_data={"cabin_temp_c": 22.0},
            power_data={"battery_soc_pct": 95.0},
            docking_data={"docking_status": "SEPARATED"},
        )

        quasim_data = adapter.export_quasim_format(telemetry)

        assert quasim_data["timestamp"] == 100.0
        assert quasim_data["source"] == "Dragon_Dragon_C210"
        assert quasim_data["trajectory"]["position"] == [6_700_000.0, 0.0, 0.0]
        assert quasim_data["trajectory"]["velocity"] == [0.0, 7500.0, 0.0]
        assert quasim_data["trajectory"]["altitude"] == 400_000.0
        assert quasim_data["gnc"]["attitude"] == [1.0, 0.0, 0.0, 0.0]
        assert quasim_data["gnc"]["mode"] == "NOMINAL"
        assert "thermal" in quasim_data["systems"]
        assert "power" in quasim_data["systems"]
        assert "docking" in quasim_data["systems"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
