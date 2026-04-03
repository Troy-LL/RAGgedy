from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent


def _default_question(path_name: str) -> str:
    # Safe starter prompts per path; override with --question.
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
    # Primary route selector: exactly one path is executed per command.
    parser.add_argument(
        "--path",
        choices=["mock", "demo", "naive", "advanced", "api", "local"],
        default="mock",
        help="Which project path to run",
    )
    # Common knobs available across most paths.
    parser.add_argument("--question", default=None, help="Question for the selected path")
    # Applies to module paths (naive/advanced) via RAGGEDY_DATASET.
    parser.add_argument("--dataset", default=os.getenv("RAGGEDY_DATASET", "edu_scholar"))
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--show-trace", action="store_true")
    parser.add_argument(
        "--visualize",
        choices=["auto", "popup", "terminal", "off"],
        default="auto",
        help="Visualization mode",
    )

    # API/local provider settings can come from env vars or CLI overrides.
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

    # If no question is provided, use a path-specific default prompt.
    question = (args.question or _default_question(args.path)).strip()

    if args.path == "demo":
        # Polished Tier-1 walkthrough script.
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

    # Module paths are mutually exclusive here: this branch routes to exactly one module.
    if args.path in {"naive", "advanced"}:
        # `--path naive` -> 01_Naive_RAG/query.py, `--path advanced` -> 02_Advanced_RAG/query.py
        target = "01_Naive_RAG/query.py" if args.path == "naive" else "02_Advanced_RAG/query.py"
        env = os.environ.copy()
        # Keep dataset selection centralized at the runner level.
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
    # mock/api/local are routed to the unified zero_barrier_runtime app.
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
        # Trace is most useful for mock mode but allowed for all runtime modes.
        cmd.append("--show-trace")

    if mode == "api":
        # Provider/model credentials are only relevant in API mode.
        cmd.extend(["--provider", args.provider, "--model", args.model, "--api-key", args.api_key])

    if mode == "local":
        # Local mode targets an Ollama-compatible endpoint/model.
        cmd.extend(["--local-base-url", args.local_base_url, "--local-model", args.local_model])

    return _run(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
