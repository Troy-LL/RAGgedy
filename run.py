from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent


def _default_question(path_name: str) -> str:
    defaults = {
        "mock": "Why does chunking help?",
        "demo": "Why does chunking help a RAG system answer better?",
        "naive": "Why does chunking help?",
        "advanced": "How does reranking improve quality?",
        "api": "Explain vector embeddings like I am 5",
        "local": "How does retrieval improve answer quality?",
    }
    return defaults[path_name]


def _run(cmd: list[str], env: dict[str, str] | None = None) -> int:
    return subprocess.call(cmd, cwd=str(REPO_ROOT), env=env)


def main() -> int:
    parser = argparse.ArgumentParser(description="Unified project runner")
    parser.add_argument(
        "--path",
        choices=["mock", "demo", "naive", "advanced", "api", "local"],
        default="mock",
        help="Which project path to run",
    )
    parser.add_argument("--question", default=None, help="Question for the selected path")
    parser.add_argument("--dataset", default=os.getenv("RAGGEDY_DATASET", "edu_scholar"))
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--show-trace", action="store_true")
    parser.add_argument(
        "--visualize",
        choices=["auto", "popup", "terminal", "off"],
        default="auto",
        help="Visualization mode",
    )

    parser.add_argument("--provider", default=os.getenv("MODEL_PROVIDER", "groq"))
    parser.add_argument("--model", default=os.getenv("MODEL_NAME", "llama-3.1-8b-instant"))
    parser.add_argument("--api-key", default=os.getenv("MODEL_API_KEY", ""))
    parser.add_argument(
        "--local-base-url",
        default=os.getenv("LOCAL_BASE_URL", "http://localhost:11434"),
    )
    parser.add_argument(
        "--local-model",
        default=os.getenv("LOCAL_MODEL_NAME", "llama3.1:8b"),
    )
    args = parser.parse_args()

    question = (args.question or _default_question(args.path)).strip()

    if args.path == "demo":
        cmd = [
            sys.executable,
            "-m",
            "zero_barrier_runtime.scripts.mock_trace_demo",
            "--question",
            question,
            "--visualize",
            args.visualize,
        ]
        return _run(cmd)

    if args.path in {"naive", "advanced"}:
        target = "01_Naive_RAG/query.py" if args.path == "naive" else "02_Advanced_RAG/query.py"
        env = os.environ.copy()
        env["RAGGEDY_DATASET"] = args.dataset
        cmd = [
            sys.executable,
            target,
            "--question",
            question,
            "--visualize",
            args.visualize,
        ]
        return _run(cmd, env=env)

    mode = args.path
    cmd = [
        sys.executable,
        "-m",
        "zero_barrier_runtime.app",
        "--mode",
        mode,
        "--question",
        question,
        "--top-k",
        str(args.top_k),
        "--visualize",
        args.visualize,
    ]

    if args.show_trace:
        cmd.append("--show-trace")

    if mode == "api":
        cmd.extend(["--provider", args.provider, "--model", args.model, "--api-key", args.api_key])

    if mode == "local":
        cmd.extend(["--local-base-url", args.local_base_url, "--local-model", args.local_model])

    return _run(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
