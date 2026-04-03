import argparse
import os


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Zero-barrier RAG runtime")
    parser.add_argument("--mode", choices=["mock", "api", "local"], default="mock")
    parser.add_argument("--question", required=True)
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--show-trace", action="store_true")
    parser.add_argument(
        "--visualize",
        choices=["auto", "popup", "terminal", "off"],
        default="auto",
        help=(
            "Display result visualization without localhost. "
            "auto=popup with terminal fallback, popup=native window, "
            "terminal=print only, off=disable output"
        ),
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
    return parser
