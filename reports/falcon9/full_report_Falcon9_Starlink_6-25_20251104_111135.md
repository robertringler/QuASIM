# QuASIM Mission Data Integration Report

**Generated:** 2025-11-04 11:11:35
**Overall Status:** ❌ FAILED

---

# Mission Data Validation Report

**Status:** ✅ PASSED
**Errors:** 0
**Warnings:** 0

## Metadata

- **mission_type:** falcon9
- **data_points_validated:** 4


---

# QuASIM Performance Comparison Report

**Mission ID:** Falcon9_Starlink_6-25
**Simulation ID:** quasim_Falcon9_Starlink_6-25
**Status:** ❌ FAILED

## Summary

- **Total Variables:** 5
- **Data Points:** 4
- **Passed Checks:** 0
- **Failed Checks:** 2
- **Average RMSE:** 1167.5624
- **Average Correlation:** 0.0000

## Failed Acceptance Criteria

- velocity: RMSE=262.20 > 50.00
- altitude: RMSE=5567.32 > 1000.00

## Detailed Metrics

| Variable | RMSE | MAE | Max Error | Correlation | Bias |
|----------|------|-----|-----------|-------------|------|
| velocity | 262.2022 | 200.0000 | 450.0000 | 0.0000 | -200.0000 |
| throttle | 5.5902 | 3.7500 | 10.0000 | 0.0000 | 3.7500 |
| thrust | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| altitude | 5567.3153 | 4050.0000 | 9900.0000 | 0.0000 | -4050.0000 |
| downrange | 2.7042 | 1.8750 | 5.0000 | 0.0000 | -1.8750 |
