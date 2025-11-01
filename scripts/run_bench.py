"""CLI wrapper to execute the QuASIM micro-benchmark.

DEPRECATED: This script is now a thin wrapper around the unified infra.py script.
Please use 'python scripts/infra.py bench' instead.
"""
from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the QuASIM benchmark harness")
    parser.add_argument("--batches", type=int, default=32)
    parser.add_argument("--rank", type=int, default=4)
    parser.add_argument("--dimension", type=int, default=2048)
    parser.add_argument("--repeat", type=int, default=5)
    return parser.parse_args()


def main() -> None:
    print("Note: run_bench.py is now a wrapper. Consider using 'python scripts/infra.py bench' directly.")
    args = parse_args()
    infra_script = REPO_ROOT / "scripts" / "infra.py"
    cmd = [sys.executable, str(infra_script), "bench"]
    cmd.extend(["--batches", str(args.batches)])
    cmd.extend(["--rank", str(args.rank)])
    cmd.extend(["--dimension", str(args.dimension)])
    cmd.extend(["--repeat", str(args.repeat)])
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
