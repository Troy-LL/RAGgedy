"""Shared launcher for module-bound visualization startup."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
APP_PATH = REPO_ROOT / "visualization" / "app.py"
SUPPORTED_MODULES = {"01_Naive_RAG", "02_Advanced_RAG"}


def _resolve_dataset(dataset: str | None) -> str:
    value = (dataset or os.getenv("RAGGEDY_DATASET", "edu_scholar")).strip()
    return value or "edu_scholar"


def launch_visualization(
    module_subdir: str,
    dataset: str | None = None,
    *,
    auto_ingest: bool = False,
    port: int | None = None,
) -> int:
    if module_subdir not in SUPPORTED_MODULES:
        supported = ", ".join(sorted(SUPPORTED_MODULES))
        raise ValueError(f"Unsupported module '{module_subdir}'. Expected one of: {supported}")

    env = os.environ.copy()
    env["RAGGEDY_VIS_MODULE"] = module_subdir
    env["RAGGEDY_DATASET"] = _resolve_dataset(dataset)
    env["RAGGEDY_VIS_AUTO_INGEST"] = "1" if auto_ingest else "0"

    cmd = [sys.executable, "-m", "streamlit", "run", str(APP_PATH)]
    if port is not None:
        cmd.extend(["--server.port", str(port)])

    return subprocess.call(cmd, cwd=str(REPO_ROOT), env=env)


def main() -> int:
    parser = argparse.ArgumentParser(description="Launch module-bound visualization")
    parser.add_argument("--module", required=True, choices=sorted(SUPPORTED_MODULES))
    parser.add_argument("--dataset", default=None)
    parser.add_argument("--auto-ingest", action="store_true")
    parser.add_argument("--port", type=int, default=None)
    args = parser.parse_args()

    return launch_visualization(
        module_subdir=args.module,
        dataset=args.dataset,
        auto_ingest=args.auto_ingest,
        port=args.port,
    )


if __name__ == "__main__":
    raise SystemExit(main())
