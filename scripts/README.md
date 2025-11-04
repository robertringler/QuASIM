# Scripts

Automation helpers for linting, simulation, coverage, and documentation rendering.

## Available Scripts

### `test_full_stack.py`

Validates the repository structure and code syntax:
- YAML/JSON file syntax validation
- Terraform module validation (if terraform CLI available)
- Python syntax validation via bytecode compilation

**Usage:**
```bash
python3 scripts/test_full_stack.py
# or
make test
```

### `sanity_check_full_stack.py`

Comprehensive full stack build and integration test:
- Validates docker-compose configuration
- Builds Docker images for all services
- Starts services and waits for health checks
- Tests backend API endpoints (health, kernel, metrics)
- Validates frontend accessibility and content
- Cleans up resources after testing

**Usage:**
```bash
# Run full sanity check (builds, tests, and cleans up)
python3 scripts/sanity_check_full_stack.py
# or
make sanity-check

# Skip Docker build (assumes services already running)
python3 scripts/sanity_check_full_stack.py --skip-docker

# Keep services running after tests
python3 scripts/sanity_check_full_stack.py --keep-running
```

**What it validates:**
- Docker Compose configuration syntax
- Docker image builds successfully
- Services start and become healthy
- Backend health endpoint returns 200 OK
- Backend kernel endpoint processes requests correctly
- Backend metrics endpoint returns Prometheus metrics
- Frontend serves HTML and contains expected content

This script is ideal for:
- Pre-commit validation
- CI/CD pipeline integration
- Pre-deployment smoke testing
- Verifying stack integrity after code changes
