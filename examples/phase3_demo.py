#!/usr/bin/env python3
"""Complete demonstration of Phase III autonomous evolution capabilities.

This script showcases all major Phase III components working together.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from evolve.init_population import generate_initial_population
from evolve.introspection_agent import IntrospectionAgent, simulate_kernel_execution
from evolve.rl_controller import RLController
from evolve.precision_controller import PrecisionController
from evolve.evolution_dashboard import EvolutionDashboard
from schedules.differentiable_scheduler import DifferentiableScheduler
from quantum_search.ising_optimizer import QuantumInspiredOptimizer
from memgraph.graph_optimizer import MemoryGraphOptimizer
from profiles.causal_profiler import CausalProfiler
from federated.intelligence import FederatedIntelligence


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def main():
    """Run comprehensive Phase III demonstration."""
    print_section("Phase III Autonomous Evolution - Complete Demo")
    
    # 1. Initialize Population
    print_section("1. Initializing Kernel Population")
    population = generate_initial_population(size=3, seed=42)
    print(f"Generated {len(population)} initial genomes")
    for i, genome in enumerate(population):
        print(f"  Genome {i+1}: tile={genome.tile_size}, warp={genome.warp_count}, "
              f"unroll={genome.unroll_factor}, async={genome.async_depth}, "
              f"precision={genome.precision}")
    
    # 2. Introspection Agent
    print_section("2. Runtime Introspection & Monitoring")
    agent = IntrospectionAgent()
    genome = population[0]
    print(f"Monitoring execution of {genome.genome_id}...")
    metrics = simulate_kernel_execution(agent, genome.genome_id, workload_complexity=2.0)
    print(f"  Latency:         {metrics.latency_ms:.3f} ms")
    print(f"  Warp Divergence: {metrics.warp_divergence_pct:.2f}%")
    print(f"  Cache Miss Rate: {metrics.cache_miss_rate:.3f}")
    print(f"  Memory BW:       {metrics.memory_bandwidth_gb_s:.1f} GB/s")
    print(f"  Energy:          {metrics.energy_consumption_j:.3f} J")
    
    # 3. RL Optimization
    print_section("3. RL-Based Kernel Optimization")
    controller = RLController()
    print(f"Optimizing {genome.genome_id} with reinforcement learning...")
    optimized = controller.optimize_kernel(genome, metrics, baseline_latency=10.0)
    print(f"  Original tile size: {genome.tile_size} → Optimized: {optimized.tile_size}")
    print(f"  Original warp count: {genome.warp_count} → Optimized: {optimized.warp_count}")
    print(f"  Fitness improvement: {genome.fitness:.3f} → {optimized.fitness:.3f}")
    
    # 4. Precision Control
    print_section("4. Hierarchical Precision Management")
    precision_ctrl = PrecisionController()
    kernel_id = genome.genome_id
    precision_map = precision_ctrl.create_hierarchical_map(kernel_id, num_layers=10)
    print(f"Created precision map with {len(precision_map.zones)} zones:")
    for zone in precision_map.zones:
        print(f"  {zone.zone_type}: {zone.precision.value} "
              f"({zone.precision.bits} bits, {zone.compute_savings_pct:.0f}% savings)")
    savings = precision_ctrl.get_compute_savings(kernel_id)
    print(f"Total compute savings: {savings:.1f}%")
    
    # 5. Differentiable Scheduling
    print_section("5. Differentiable Compiler Scheduling")
    scheduler = DifferentiableScheduler()
    schedule = scheduler.create_schedule(f"{kernel_id}_schedule", kernel_id)
    print(f"Optimizing schedule with gradient descent...")
    optimized_schedule = scheduler.optimize_schedule(schedule, iterations=50, 
                                                     target_latency=metrics.latency_ms)
    print(f"  Final latency: {optimized_schedule.latency_ms:.3f} ms")
    print(f"  Final energy:  {optimized_schedule.energy_j:.3f} J")
    print(f"  Final loss:    {optimized_schedule.loss:.6f}")
    
    # 6. Quantum-Inspired Search
    print_section("6. Quantum-Inspired Configuration Search")
    quantum_opt = QuantumInspiredOptimizer()
    print(f"Running simulated annealing on Ising model...")
    optimal_params = quantum_opt.optimize_kernel_config(kernel_id, iterations=500)
    print(f"Optimal parameters found:")
    for param, value in optimal_params.items():
        print(f"  {param}: {value}")
    
    # 7. Memory Graph Optimization
    print_section("7. Topological Memory Graph Optimization")
    mem_optimizer = MemoryGraphOptimizer()
    mem_graph = mem_optimizer.create_memory_graph(kernel_id, num_tensors=6)
    print(f"Created memory graph: {len(mem_graph.nodes)} nodes, {len(mem_graph.edges)} edges")
    print(f"Total memory: {mem_graph.total_memory_bytes / (1024*1024):.2f} MB")
    optimized_graph = mem_optimizer.optimize_layout(mem_graph)
    print(f"Optimized layout with GNN:")
    print(f"  Cache miss rate: {optimized_graph.cache_miss_rate:.3f}")
    print(f"  Improvement:     {(0.15 - optimized_graph.cache_miss_rate) / 0.15 * 100:.1f}%")
    
    # 8. Causal Profiling
    print_section("8. Causal Profiling & Critical Path Analysis")
    profiler = CausalProfiler()
    functions = [f"{kernel_id}_func_{i}" for i in range(5)]
    profile = profiler.profile_kernel(kernel_id, functions=functions, perturbation_ms=0.5)
    critical_path = profile.get_critical_path()
    print(f"Critical path (by causal impact):")
    for i, func in enumerate(critical_path[:3], 1):
        influence = next(inf for inf in profile.influences if inf.function_name == func)
        print(f"  {i}. {func}: impact score = {influence.causal_impact:.3f}")
    
    # 9. Federated Intelligence
    print_section("9. Federated Kernel Intelligence")
    intel = FederatedIntelligence()
    print("Submitting telemetry...")
    intel.submit_telemetry(
        deployment_name="demo_deployment",
        kernel_family="compute",
        params=optimal_params,
        latency_ms=metrics.latency_ms,
        throughput=1000.0 / metrics.latency_ms,
        hardware_class="gpu_high"
    )
    predictor = intel.train_predictor("compute")
    print(f"Trained predictor: {predictor.training_samples} samples")
    predicted = intel.query_predictor("compute", optimal_params, "gpu_high")
    print(f"Predicted latency for optimal config: {predicted:.2f} ms")
    
    # 10. Evolution Dashboard
    print_section("10. Evolution Progress Dashboard")
    dashboard = EvolutionDashboard()
    # Simulate some evolution progress
    for gen in range(3):
        pop_metrics = [
            {"latency_ms": 10.0 - gen * 2, "energy_j": 1.0 - gen * 0.2, "fitness": 1.0 + gen * 0.5}
            for _ in range(3)
        ]
        dashboard.record_generation(gen, pop_metrics)
    
    print(dashboard.generate_report())
    
    # Summary
    print_section("Demo Complete")
    print("All Phase III components demonstrated successfully!")
    print("\nKey achievements:")
    print(f"  ✓ RL optimization: {abs(optimized.tile_size - genome.tile_size)} parameter changes")
    print(f"  ✓ Precision savings: {savings:.1f}%")
    print(f"  ✓ Schedule optimization: {optimized_schedule.iteration} iterations")
    print(f"  ✓ Quantum search: found optimal configuration")
    print(f"  ✓ Memory optimization: {(0.15 - optimized_graph.cache_miss_rate) / 0.15 * 100:.1f}% miss rate reduction")
    print(f"  ✓ Causal profiling: identified {len(critical_path)} critical functions")
    print(f"  ✓ Federated learning: predictor trained with {predictor.training_samples} samples")
    print(f"  ✓ Evolution tracking: {len(dashboard.metrics_history)} generations recorded")
    print("\nFor full evolution cycle, run: python evolve/phase3_orchestrator.py")


if __name__ == "__main__":
    main()
