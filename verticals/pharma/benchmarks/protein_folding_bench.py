"""Benchmark: Protein folding molecular dynamics."""
from __future__ import annotations

import time
import argparse
import numpy as np
from core import Config, PrecisionMode, Backend


def benchmark_protein_folding(
    n_atoms: int = 1000,
    timesteps: int = 10000,
    backend: str = "cpu",
    quick: bool = False
):
    """
    Benchmark molecular dynamics performance.
    
    Args:
        n_atoms: Number of atoms in the protein
        timesteps: Number of MD timesteps
        backend: Backend to use (cpu, cuda, hip)
        quick: Run quick benchmark with reduced parameters
    """
    from verticals.pharma.examples.molecular_dynamics_example import MolecularDynamicsKernel
    
    if quick:
        n_atoms = 100
        timesteps = 1000
    
    # Create random protein structure
    protein = np.random.rand(n_atoms, 3) * 10.0
    
    # Configure kernel
    backend_map = {"cpu": Backend.CPU, "cuda": Backend.CUDA, "hip": Backend.HIP}
    config = Config(
        precision=PrecisionMode.FP32,
        backend=backend_map.get(backend, Backend.CPU),
        enable_telemetry=True
    )
    
    kernel = MolecularDynamicsKernel(config)
    
    # Warmup
    kernel.execute(protein[:10], timesteps=10)
    
    # Benchmark
    start = time.perf_counter()
    result = kernel.execute(protein, timesteps=timesteps)
    elapsed = time.perf_counter() - start
    
    # Calculate metrics
    timesteps_per_sec = timesteps / elapsed
    ns_per_day = (timesteps * 0.002) / elapsed * 86400 / 1000  # Assuming 2fs timestep
    
    print(f"\n{'='*60}")
    print(f"Protein Folding MD Benchmark")
    print(f"{'='*60}")
    print(f"Configuration:")
    print(f"  Atoms: {n_atoms}")
    print(f"  Timesteps: {timesteps}")
    print(f"  Backend: {backend}")
    print(f"  Precision: {config.precision.value}")
    print(f"\nPerformance:")
    print(f"  Total time: {elapsed:.3f} s")
    print(f"  Timesteps/sec: {timesteps_per_sec:.1f}")
    print(f"  ns/day: {ns_per_day:.2f}")
    print(f"  Final energy: {result['energies'][-1]:.4f}")
    print(f"\nTarget: 2.0× speedup vs baseline (>10,000 timesteps/sec)")
    print(f"Status: {'PASS' if timesteps_per_sec > 10000 else 'NEEDS OPTIMIZATION'}")
    print(f"{'='*60}\n")
    
    return {
        'elapsed_sec': elapsed,
        'timesteps_per_sec': timesteps_per_sec,
        'ns_per_day': ns_per_day,
        'backend': backend,
        'n_atoms': n_atoms
    }


def main():
    parser = argparse.ArgumentParser(description="Protein folding benchmark")
    parser.add_argument('--atoms', type=int, default=1000, help='Number of atoms')
    parser.add_argument('--timesteps', type=int, default=10000, help='Number of timesteps')
    parser.add_argument('--backend', type=str, default='cpu', choices=['cpu', 'cuda', 'hip'])
    parser.add_argument('--quick', action='store_true', help='Run quick benchmark')
    
    args = parser.parse_args()
    
    benchmark_protein_folding(
        n_atoms=args.atoms,
        timesteps=args.timesteps,
        backend=args.backend,
        quick=args.quick
    )


if __name__ == "__main__":
    main()
