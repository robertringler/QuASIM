"""Launch behavioral simulations for the GB10 top-level RTL.

DEPRECATED: This script is now a thin wrapper around the unified infra.py script.
Please use 'python scripts/infra.py sim' instead.
"""
from __future__ import annotations

import pathlib
import subprocess
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


def main() -> None:
    print("Note: run_sim.py is now a wrapper. Consider using 'python scripts/infra.py sim' directly.")
    infra_script = REPO_ROOT / "scripts" / "infra.py"
    subprocess.run([sys.executable, str(infra_script), "sim"], check=True)


if __name__ == "__main__":
    main()
