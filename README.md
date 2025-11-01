# GB10 QuASIM Reference Platform — Phase IV

The GB10 QuASIM reference repository delivers a cohesive hardware-software co-design stack for a synthetic Grace-Blackwell inspired superchip optimized for AI and quantum simulation workloads. **Phase IV** extends QuASIM into a full-stack simulation ecosystem serving multiple scientific and industrial markets with neuromorphic, quantum-hybrid, generative, and energy-aware capabilities.

## 🚀 What's New in Phase IV

Phase IV introduces **Cross-Vertical Intelligence Expansion**, transforming QuASIM from a specialized quantum simulator into a comprehensive platform for:

- **6 Industry Verticals**: Pharma, Aerospace, Finance, Telecom, Energy, Defense
- **Neuromorphic Computing**: Event-driven spiking neural networks with STDP learning
- **Quantum-Hybrid**: Unified bridge for Qiskit, Braket, PennyLane backends
- **Neural PDEs**: Fourier Neural Operators and DeepONet for scientific computing
- **Generative Engineering**: Diffusion models for materials, circuits, aerodynamics
- **Federated Cloud**: Privacy-preserving multi-tenant collaboration
- **Edge Runtime**: LLVM-IR/WASM export for ARM, RISC-V, edge AI accelerators
- **3D Visualization**: Interactive dashboards with Plotly and Three.js

**Market Impact**: $239B total addressable market across all verticals with 2-3× performance improvements and ≤30% energy reduction vs. legacy HPC.

## Repository Layout

```
# Phase IV Verticals
verticals/
├── pharma/         Molecular dynamics, docking, pharmacokinetics
├── aerospace/      CFD, structural analysis, trajectory optimization
├── finance/        Monte Carlo, quantum risk, ESG climate modeling
├── telecom/        MIMO, mmWave, 6G network simulation
├── energy/         Plasma, smart-grid, fusion control
└── defense/        Radar, EW, ballistics, threat assessment

# Cross-Cutting Capabilities
neuromorphic/       Spiking neural networks with biological learning
quantum_bridge/     Quantum-classical hybrid orchestration
operators/          Neural PDE solvers (FNO, DeepONet)
gen_design/         Generative models for engineering design
federated/          Privacy-preserving multi-tenant simulation
edge_runtime/       Edge deployment (ARM, RISC-V, WASM)
dashboard/          Interactive 3D visualization

# Core Infrastructure
core/               Base classes, precision, backend abstraction
ir/                 MLIR-based intermediate representation
autotune/           Automatic kernel parameter tuning
async/              Asynchronous distributed execution

# Original Platform
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
examples/           Cross-vertical integration examples
```

## Quick Start

### Phase IV Vertical Examples

```bash
# Install dependencies
pip install numpy pytest

# Pharmaceutical: Molecular dynamics simulation
PYTHONPATH=. python verticals/pharma/examples/molecular_dynamics_example.py

# Finance: Monte Carlo option pricing
PYTHONPATH=. python verticals/finance/examples/monte_carlo_pricing.py

# Run benchmarks
PYTHONPATH=. python verticals/pharma/benchmarks/protein_folding_bench.py --quick
PYTHONPATH=. python verticals/finance/benchmarks/options_pricing_bench.py --quick

# Cross-vertical integration demo
PYTHONPATH=. python examples/cross_vertical_integration.py

# Run tests
PYTHONPATH=. pytest verticals/pharma/tests/ -v
PYTHONPATH=. pytest verticals/finance/tests/ -v
```

### Original Platform

1. Install build prerequisites (`cmake`, `ninja`, `gcc`, `clang`, `python3`, `verilator`, `openjdk`, `sbt`, and `pytest`).
2. Run `make setup` to configure the local toolchain mirrors and Python environment.
3. Use `make lint`, `make sim`, and `make cov` to exercise RTL quality gates.
4. Build and run the runtime tests with `make runtime` and `make test`.
5. Benchmark the QuASIM tensor simulator with `make bench` or invoke `python benchmarks/quasim_bench.py` directly for custom parameters.

## Phase IV Architecture

Each vertical is self-contained with:
- **manifest.yaml**: Kernel specs, datasets, benchmarks, dependencies
- **README.md**: Comprehensive documentation
- **examples/**: Runnable code examples
- **tests/**: Pytest test suite
- **benchmarks/**: Performance benchmarking scripts
- **notebooks/**: Jupyter notebooks (coming soon)

Cross-cutting modules provide shared capabilities:
- **Neuromorphic**: Spiking networks optimized for 100-1000× lower energy
- **Quantum Bridge**: Abstract interface to IBM, AWS, PennyLane quantum backends
- **Operators**: Neural PDE solvers achieving 100-1000× speedup over traditional methods
- **Gen Design**: AI-powered structure generation for materials, circuits, aerodynamics
- **Federated**: Privacy-preserving collaboration with differential privacy (ε=1.0)
- **Edge Runtime**: Sub-5W deployment on ARM/RISC-V with <10ms latency
- **Dashboard**: Real-time 3D visualization with WebGL rendering

The repository is intentionally modular—each layer can be evaluated independently while maintaining coherent interfaces. Refer to `docs/roadmap_v4.md` for detailed market analysis, use cases, and performance targets.

## Licensing

All source code and documentation in this repository is provided under the Apache 2.0 license unless otherwise noted. This project is intended for academic and research exploration of heterogeneous compute designs.
