"""Benchmark: Options pricing Monte Carlo performance."""
from __future__ import annotations

import time
import argparse
import numpy as np
from core import Config, PrecisionMode, Backend


def benchmark_options_pricing(
    n_paths: int = 1_000_000,
    n_options: int = 100,
    backend: str = "cpu",
    quick: bool = False
):
    """
    Benchmark Monte Carlo option pricing performance.
    
    Args:
        n_paths: Number of Monte Carlo paths per option
        n_options: Number of options to price
        backend: Backend to use (cpu, cuda, hip)
        quick: Run quick benchmark with reduced parameters
    """
    from verticals.finance.examples.monte_carlo_pricing import MonteCarloOptionPricer
    
    if quick:
        n_paths = 10_000
        n_options = 10
    
    # Configure kernel
    backend_map = {"cpu": Backend.CPU, "cuda": Backend.CUDA, "hip": Backend.HIP}
    config = Config(
        precision=PrecisionMode.FP64,
        backend=backend_map.get(backend, Backend.CPU),
        enable_telemetry=True
    )
    
    pricer = MonteCarloOptionPricer(config)
    
    # Generate random option parameters
    spots = np.random.uniform(80, 120, n_options)
    strikes = np.random.uniform(90, 110, n_options)
    volatilities = np.random.uniform(0.15, 0.35, n_options)
    
    # Warmup
    pricer.execute(100.0, 100.0, 0.05, 0.2, 1.0, n_paths=1000)
    
    # Benchmark
    start = time.perf_counter()
    
    results = []
    for i in range(n_options):
        result = pricer.execute(
            spot=spots[i],
            strike=strikes[i],
            rate=0.05,
            volatility=volatilities[i],
            maturity=1.0,
            n_paths=n_paths,
            option_type="call"
        )
        results.append(result)
    
    elapsed = time.perf_counter() - start
    
    # Calculate metrics
    total_paths = n_paths * n_options
    paths_per_sec = total_paths / elapsed
    options_per_sec = n_options / elapsed
    
    # Calculate average pricing accuracy
    avg_std_error = np.mean([r['std_error'] for r in results])
    avg_price = np.mean([r['price'] for r in results])
    relative_error = avg_std_error / avg_price if avg_price > 0 else 0
    
    print(f"\n{'='*60}")
    print(f"Monte Carlo Options Pricing Benchmark")
    print(f"{'='*60}")
    print(f"Configuration:")
    print(f"  Options priced: {n_options}")
    print(f"  Paths per option: {n_paths:,}")
    print(f"  Total paths: {total_paths:,}")
    print(f"  Backend: {backend}")
    print(f"  Precision: {config.precision.value}")
    print(f"\nPerformance:")
    print(f"  Total time: {elapsed:.3f} s")
    print(f"  Options/sec: {options_per_sec:.1f}")
    print(f"  Paths/sec: {paths_per_sec:,.0f}")
    print(f"  Time per option: {elapsed/n_options*1000:.2f} ms")
    print(f"\nAccuracy:")
    print(f"  Average price: ${avg_price:.4f}")
    print(f"  Average std error: ${avg_std_error:.4f}")
    print(f"  Relative error: {relative_error:.4%}")
    print(f"\nTarget: 3.0× speedup (>1M paths/sec)")
    print(f"Status: {'PASS' if paths_per_sec > 1_000_000 else 'NEEDS OPTIMIZATION'}")
    print(f"{'='*60}\n")
    
    return {
        'elapsed_sec': elapsed,
        'paths_per_sec': paths_per_sec,
        'options_per_sec': options_per_sec,
        'relative_error': relative_error,
        'backend': backend
    }


def main():
    parser = argparse.ArgumentParser(description="Options pricing benchmark")
    parser.add_argument('--paths', type=int, default=1_000_000, help='Paths per option')
    parser.add_argument('--options', type=int, default=100, help='Number of options')
    parser.add_argument('--backend', type=str, default='cpu', choices=['cpu', 'cuda', 'hip'])
    parser.add_argument('--quick', action='store_true', help='Run quick benchmark')
    
    args = parser.parse_args()
    
    benchmark_options_pricing(
        n_paths=args.paths,
        n_options=args.options,
        backend=args.backend,
        quick=args.quick
    )


if __name__ == "__main__":
    main()
