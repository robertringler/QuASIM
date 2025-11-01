# Phase III Examples

This directory contains demonstration scripts for Phase III autonomous evolution capabilities.

## Available Demos

### phase3_demo.py

Comprehensive demonstration of all Phase III components:

```bash
python examples/phase3_demo.py
```

This demo showcases:

1. **Kernel Population Initialization**: Generate diverse initial genomes
2. **Runtime Introspection**: Monitor execution metrics
3. **RL-Based Optimization**: Improve kernel parameters
4. **Precision Management**: Hierarchical mixed-precision optimization
5. **Differentiable Scheduling**: Gradient-based schedule optimization
6. **Quantum-Inspired Search**: Configuration space exploration
7. **Memory Graph Optimization**: GNN-based layout optimization
8. **Causal Profiling**: Critical path identification
9. **Federated Intelligence**: Cross-deployment learning
10. **Evolution Dashboard**: Progress tracking and visualization

## Full Evolution Cycle

For a complete evolution cycle with multiple generations:

```bash
python evolve/phase3_orchestrator.py
```

This runs:
- Population initialization
- Multi-generation evolution
- All optimization subsystems
- Comprehensive metrics tracking
- Success criteria validation

## Individual Component Demos

Run individual component demos directly:

```bash
# Introspection agent
python evolve/introspection_agent.py

# RL controller
python evolve/rl_controller.py

# Precision controller
python evolve/precision_controller.py

# Differentiable scheduler
python schedules/differentiable_scheduler.py

# Quantum optimizer
python quantum_search/ising_optimizer.py

# Memory graph optimizer
python memgraph/graph_optimizer.py

# Causal profiler
python profiles/causal_profiler.py

# Federated intelligence
python federated/intelligence.py

# Evolution dashboard
python evolve/evolution_dashboard.py
```

## Output

All demos generate output in appropriate directories:

- `evolve/genomes/` - Kernel genome files
- `evolve/policies/` - RL policy checkpoints
- `schedules/` - Optimized schedules
- `schedules/precision_maps/` - Precision maps
- `quantum_search/` - Optimization histories
- `memgraph/` - Memory graphs
- `profiles/causal/` - Causal influence maps
- `profiles/introspection/` - Performance metrics
- `profiles/evolution/` - Evolution dashboards
- `federated/` - Telemetry and predictors

## Testing

Run the comprehensive test suite:

```bash
PYTHONPATH=. pytest tests/software/test_phase3.py -v
```

## Documentation

See detailed documentation in:
- [Phase III Overview](../docs/phase3_autonomous_evolution.md)
- [Evolution README](../evolve/README.md)
