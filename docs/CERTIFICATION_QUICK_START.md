# Certification Pipeline Quick Start

## For Developers

### What Gets Checked on Every PR?

When you submit a pull request, the **Certification CI/CD Pipeline** automatically validates:

✅ **Monte-Carlo Fidelity** - Quantum simulation accuracy (≥ 0.97 ± 0.005)  
✅ **MC/DC Coverage** - Complete test coverage per DO-178C (100%)  
✅ **Anomaly Check** - No open issues in certification package (0 anomalies)  
✅ **Package Integrity** - All verification evidence items present  

**These checks must pass before your PR can be merged.**

### Running Tests Locally Before Pushing

```bash
# 1. Install dependencies
pip install pytest qutip numpy scipy pytest-json-report pytest-html

# 2. Generate certification artifacts
python generate_quasim_jsons.py

# 3. Run all certification tests
pytest test_quasim_validator.py -v

# 4. Optional: Run QuASIM validation suite
pytest validation_suite.py -v
```

### Understanding PR Comments

After the pipeline runs, you'll see a comment on your PR with results:

```
## 🔬 Certification Validation Results

### Monte-Carlo Fidelity
- Mean Fidelity: 0.970470
- Target: 0.97 ± 0.005
- Convergence Rate: 98.54%
- Status: ✅ PASSED

### MC/DC Coverage
- Standard: DO-178C §6.4.4
- Coverage: 100% (200/200 conditions)
- Status: ✅ PASSED

### Anomaly Check
- Open Anomalies: 0
- Verification Status: READY_FOR_AUDIT
- Status: ✅ PASSED
```

### What If Tests Fail?

#### Fidelity Failure

```
❌ GATE FAILED: Mean fidelity 0.965 below threshold 0.97
```

**Fix**: Your changes may have introduced numerical instability. Check:
- Quantum simulation parameters
- Noise modeling changes
- Numerical precision settings

#### Coverage Failure

```
❌ GATE FAILED: MC/DC coverage incomplete (195/200 conditions)
```

**Fix**: Add test cases for uncovered code paths:
```bash
# Find uncovered conditions
grep "False" montecarlo_campaigns/coverage_matrix.csv
```

#### Anomaly Failure

```
❌ GATE FAILED: Open anomalies detected (3 found)
```

**Fix**: Review and close open issues in the certification package:
```bash
# Check anomaly details
cat cdp_artifacts/CDP_v1.0.json | jq '.package.open_anomalies'
```

### Quick Validation Check

Before pushing, run this one-liner to verify all gates pass:

```bash
python generate_quasim_jsons.py && \
pytest test_quasim_validator.py -v && \
echo "✅ All certification gates passed locally!"
```

### Viewing Artifacts

After the pipeline runs, you can download artifacts from the GitHub Actions page:

1. Go to your PR
2. Click "Checks" tab
3. Click "Certification CI/CD Pipeline"
4. Scroll to "Artifacts" section
5. Download `certification-artifacts` or `certification-test-reports`

### Common Questions

**Q: Do I need to commit generated artifacts?**  
A: No, the pipeline generates them automatically. Only commit source code changes.

**Q: Can I skip certification tests for documentation-only changes?**  
A: No, all PRs must pass certification tests to ensure baseline compliance.

**Q: How long does the pipeline take?**  
A: Typically 15-20 seconds for the complete pipeline.

**Q: What if I'm working on a feature branch?**  
A: The pipeline only runs on PRs to main/master. Develop freely on feature branches.

## For Release Managers

### Creating a Release with Certification Bundle

1. Create and push a tag:
```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

2. Create release on GitHub:
   - Go to repository → Releases → "Draft a new release"
   - Select the tag
   - Fill in release notes
   - Publish release

3. The pipeline automatically:
   - Generates certification bundle
   - Creates `QuASIM-CDP-v1.0.0.tar.gz`
   - Attaches to release
   - Retains for 365 days

### What's in the Release Bundle?

```
QuASIM-CDP-v1.0.0.tar.gz
├── MC_Results_1024.json          # Monte-Carlo simulation results
├── coverage_matrix.csv            # MC/DC coverage data
├── seed_audit.log                 # Determinism audit log
├── CDP_v1.0.json                  # Certification Data Package
├── certification-report.json      # Test results (JSON)
├── certification-report.html      # Test results (HTML)
└── MANIFEST.txt                   # Bundle metadata
```

### Accessing Historical Artifacts

Release bundles are retained for 365 days and can be accessed:

1. Go to repository → Actions
2. Filter by "Certification CI/CD Pipeline"
3. Click on a workflow run
4. Download "release-certification-bundle-{version}"

Or download directly from releases:

```bash
wget https://github.com/YOUR_ORG/QuASIM/releases/download/v1.0.0/QuASIM-CDP-v1.0.0.tar.gz
```

## Standards References

- **DO-178C Level A**: Critical software for aerospace systems
- **ECSS-Q-ST-80C Rev. 2**: European Space Agency software assurance
- **NASA E-HBK-4008**: NASA software safety requirements

For detailed information, see [CERTIFICATION_CICD.md](CERTIFICATION_CICD.md).
