# Scripts

Automation helpers for linting, simulation, coverage, and documentation rendering.

## Unified Infrastructure Script

The `infra.py` script provides a unified full-stack infrastructure management interface for all GB10 QuASIM operations:

```bash
# Run individual operations
python scripts/infra.py lint              # Run linting checks
python scripts/infra.py sim               # Run RTL simulation
python scripts/infra.py cov               # Generate coverage report
python scripts/infra.py bench             # Run QuASIM benchmark
python scripts/infra.py docs              # Build documentation

# Run all operations in sequence
python scripts/infra.py all               # Run complete infrastructure stack
python scripts/infra.py all --continue-on-error  # Continue even if a step fails

# Run with custom parameters
python scripts/infra.py bench --batches 64 --rank 8 --dimension 4096
```

## Legacy Scripts (Deprecated)

The following individual scripts are now thin wrappers around `infra.py` and maintained for backward compatibility:
- `lint.py` - Static analysis (use `infra.py lint` instead)
- `run_sim.py` - RTL simulation (use `infra.py sim` instead)
- `run_cov.py` - Coverage generation (use `infra.py cov` instead)
- `run_bench.py` - Benchmark execution (use `infra.py bench` instead)
- `build_docs.py` - Documentation building (use `infra.py docs` instead)
