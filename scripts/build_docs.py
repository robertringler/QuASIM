"""Render Markdown documentation and validate links.

DEPRECATED: This script is now a thin wrapper around the unified infra.py script.
Please use 'python scripts/infra.py docs' instead.
"""
from __future__ import annotations

import pathlib
import subprocess
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


def main() -> None:
    print("Note: build_docs.py is now a wrapper. Consider using 'python scripts/infra.py docs' directly.")
    infra_script = REPO_ROOT / "scripts" / "infra.py"
    subprocess.run([sys.executable, str(infra_script), "docs"], check=True)


if __name__ == "__main__":
    main()
