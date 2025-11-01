# GB10 QuASIM Reference Platform

The GB10 QuASIM reference repository delivers a cohesive hardware-software co-design stack for a synthetic Grace-Blackwell inspired superchip optimized for AI and quantum simulation workloads. The project demonstrates how an open research platform could expose heterogeneous compute resources through a unified runtime and SDK.

## Repository Layout

```
rtl/                SystemVerilog and Chisel sources for the SoC
fw/                 Boot ROM, firmware, and board support libraries
drivers/            Linux kernel drivers for each subsystem
runtime/            libquasim runtime, Python bindings, and tooling
sdk/                Compiler frontend, ISA tools, and profiling utilities
tests/              Verification testbenches and software regression suites
quantum/            QuASIM accelerated kernels and visualization assets
scripts/            Build, lint, simulation, and CI orchestration scripts
docs/               Technical documentation and specifications
ci/                 Continuous integration workflows and container recipes
Makefile            Top-level convenience targets for developers
```

## Getting Started

1. Install build prerequisites (`cmake`, `ninja`, `gcc`, `clang`, `python3`, `verilator`, `openjdk`, `sbt`, and `pytest`).
2. Run `make setup` to configure the local toolchain mirrors and Python environment.
3. Use `make lint`, `make sim`, and `make cov` to exercise RTL quality gates.
4. Build and run the runtime tests with `make runtime` and `make test`.
5. Benchmark the QuASIM tensor simulator with `make bench` or invoke `python scripts/infra.py bench` directly for custom parameters.

### Unified Infrastructure Script

All infrastructure operations are now consolidated in a single script for convenience:

```bash
python scripts/infra.py lint      # Run linting checks
python scripts/infra.py sim       # Run RTL simulation
python scripts/infra.py cov       # Generate coverage report
python scripts/infra.py bench     # Run QuASIM benchmark
python scripts/infra.py docs      # Build documentation
python scripts/infra.py all       # Run all operations in sequence
```

The repository is intentionally modular—each layer can be evaluated independently while maintaining coherent interfaces. Refer to the documentation in `docs/` for in-depth architecture, firmware boot flows, and API references.

## Licensing

All source code and documentation in this repository is provided under the Apache 2.0 license unless otherwise noted. This project is intended for academic and research exploration of heterogeneous compute designs.
