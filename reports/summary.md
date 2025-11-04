# QuASIM Benchmark Report

## Environment

- **Commit**: `1d646b8c`
- **Branch**: `copilot/execute-quasim-benchmark-suite-again`
- **Dirty**: False

- **OS**: Linux
- **Python**: 3.12.3


## Summary

- **Total Kernels**: 3
- **Successful**: 3
- **Failed**: 0

## Performance Leaderboard

| Kernel | Backend | Precision | p50 (ms) | p90 (ms) | Throughput (ops/s) |
| --- | --- | --- | --- | --- | --- |
| autonomous_systems | cpu | fp32 | 0.011 | 0.012 | 88454.87 |
| quasim_runtime | cpu | fp32 | 38.393 | 38.763 | 25.98 |
| pressure_poisson | cpu | fp32 | 43.663 | 43.862 | 22.90 |

## Resource Usage

No memory data available.

## Key Findings

- **Fastest Kernel**: `autonomous_systems` (0.011 ms p50)
- **Highest Throughput**: `autonomous_systems` (88454.87 ops/s)

## Recommendations

- **Precision Testing**: Consider testing additional precisions (FP16, FP8) for speed vs. accuracy trade-offs.
