#!/usr/bin/env python3
"""Prove the repository remains valid when copied outside its checkout."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IGNORED = shutil.ignore_patterns(".git", ".venv", "__pycache__", "*.pyc")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="merge-when-awesome-copy-") as raw_tmp:
        copied = Path(raw_tmp) / "merge-when-awesome"
        shutil.copytree(ROOT, copied, ignore=IGNORED)
        process = subprocess.run(
            ["python3", "scripts/validate.py"],
            cwd=copied,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if process.returncode != 0:
            print(process.stdout, end="")
            return process.returncode

    print("Portable copy validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
