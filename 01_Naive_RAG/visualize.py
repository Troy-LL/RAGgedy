from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from visualization.launcher import launch_visualization


def main() -> int:
    parser = argparse.ArgumentParser(description="Launch visualization for 01_Naive_RAG")
    parser.add_argument("--dataset", default=None, help="Dataset id, e.g. edu_scholar")
    parser.add_argument("--auto-ingest", action="store_true", help="Run ingest automatically")
    parser.add_argument("--port", type=int, default=None, help="Streamlit server port")
    args = parser.parse_args()

    return launch_visualization(
        module_subdir="01_Naive_RAG",
        dataset=args.dataset,
        auto_ingest=args.auto_ingest,
        port=args.port,
    )


if __name__ == "__main__":
    raise SystemExit(main())
