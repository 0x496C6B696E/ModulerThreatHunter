#!/usr/bin/env python3
"""
Coordinator CLI for Moduler Threat Hunter
Usage:
  python coordinator/cli.py list
  python coordinator/cli.py run --module python
"""

import argparse
import subprocess
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULES_DIR = ROOT / "modules"

def list_modules():
    modules = [p.name for p in sorted(MODULES_DIR.iterdir()) if p.is_dir()]
    if not modules:
        print("No modules found. Create folders under 'modules/'.")
        return
    print("Available modules:")
    for m in modules:
        print(" -", m)

def run_module(name):
    path = MODULES_DIR / name
    if not path.exists():
        print(f"Module '{name}' not found under {MODULES_DIR}")
        return 1
    # Prefer run.sh; fallback to run.py or instructions in README
    run_sh = path / "run.sh"
    run_py = path / "run.py"
    if run_sh.exists():
        print(f"Running {run_sh} ...")
        return subprocess.call(["bash", str(run_sh)], cwd=str(path))
    elif run_py.exists():
        print(f"Running {run_py} with python ...")
        return subprocess.call([sys.executable, str(run_py)], cwd=str(path))
    else:
        print("No run.sh or run.py found. Open module README for instructions.")
        return 2

def describe_module(name):
    path = MODULES_DIR / name
    readme = path / "README.md"
    if readme.exists():
        print(readme.read_text())
    else:
        print("No README.md for module.")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("action", choices=["list", "run", "describe"])
    p.add_argument("--module", "-m", help="module name for run/describe")
    args = p.parse_args()

    if args.action == "list":
        list_modules()
    elif args.action == "run":
        if not args.module:
            print("Provide --module MODULE_NAME")
            return
        rc = run_module(args.module)
        if rc not in (0, None):
            sys.exit(rc)
    elif args.action == "describe":
        if not args.module:
            print("Provide --module MODULE_NAME")
            return
        describe_module(args.module)

if __name__ == "__main__":
    main()
