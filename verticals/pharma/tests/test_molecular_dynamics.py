"""Tests for molecular dynamics kernel."""
from __future__ import annotations

import numpy as np
import pytest
from core import Config, PrecisionMode, Backend


def test_molecular_dynamics_import():
    """Test that we can import the molecular dynamics example."""
    from verticals.pharma.examples.molecular_dynamics_example import MolecularDynamicsKernel
    assert MolecularDynamicsKernel is not None


def test_molecular_dynamics_basic():
    """Test basic molecular dynamics simulation."""
    from verticals.pharma.examples.molecular_dynamics_example import MolecularDynamicsKernel
    
    # Create small test system
    protein = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
    
    config = Config(
        precision=PrecisionMode.FP32,
        backend=Backend.CPU,
        enable_telemetry=True
    )
    
    kernel = MolecularDynamicsKernel(config)
    result = kernel.execute(protein, timesteps=10)
    
    assert 'trajectory' in result
    assert 'energies' in result
    assert 'final_structure' in result
    assert result['trajectory'].shape == (10, 3, 3)
    assert len(result['energies']) == 10
    assert len(kernel.telemetry) > 0


def test_molecular_dynamics_convergence():
    """Test that MD simulation produces reasonable energy trends."""
    from verticals.pharma.examples.molecular_dynamics_example import MolecularDynamicsKernel
    
    protein = np.random.rand(50, 3) * 5.0
    kernel = MolecularDynamicsKernel()
    result = kernel.execute(protein, timesteps=100)
    
    # Energy should be finite
    assert np.all(np.isfinite(result['energies']))
    
    # Final structure should be different from initial
    assert not np.allclose(result['final_structure'], protein)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
