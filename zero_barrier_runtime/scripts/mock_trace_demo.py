import argparse
import textwrap
import time

from zero_barrier_runtime.src.modes.mock_mode import build_mock_orchestrator
from zero_barrier_runtime.src.core.visualization import render_text


HEADER = """
==================== TIER 1: THEORETICAL SANDBOX ====================
This is a simulated walkthrough.
No external APIs. No local model runtime. Pure learning mode.
======================================================================
""".strip()


def type_line(line: str, delay: float = 0.02):
    for ch in line:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()


def _compose_demo_text(question: str, bundle) -> str:
    lines = [HEADER, "", f"Learner asks: {question}", "", "[Thoughts | Actions | Results]", ""]
    for step in bundle.trace:
        lines.append(step)

    lines.append("")
    lines.append("[Retrieved Cards]")
    for i, chunk in enumerate(bundle.chunks, 1):
        wrapped = textwrap.fill(chunk.text, width=72, subsequent_indent="      ")
        lines.append(f"{i}. {chunk.source}  (score={chunk.score:.3f})")
        lines.append(f"   {wrapped}")

    lines.append("")
    lines.append("[Final Answer]")
    lines.append(textwrap.fill(bundle.answer, width=76))
    lines.append("")
    lines.append("[Why this matters]")
    lines.append("- You can see the RAG lifecycle before touching model infra.")
    lines.append("- You can teach the concept live in under two minutes.")
    return "\n".join(lines)


def run_demo(question: str, visualize: str):
    orchestrator = build_mock_orchestrator()
    bundle = orchestrator.ask(question, top_k=3, include_trace=True)

    if visualize == "off":
        return

    if visualize in {"auto", "popup"}:
        # Popup-first presentation; `auto` falls back to terminal if popup is unavailable.
        render_text(
            _compose_demo_text(question, bundle),
            visualize,
            title="RAGgedy Mock Trace Demo",
            header="Tier 1 Theoretical Sandbox",
        )
        return

    print(HEADER)
    print()
    type_line(f"Learner asks: {question}", delay=0.01)
    time.sleep(0.2)

    print("\n[Thoughts | Actions | Results]\n")
    for step in bundle.trace:
        tag = step.split(":", 1)[0]
        message = step.split(":", 1)[1].strip() if ":" in step else step
        type_line(f"{tag}: {message}", delay=0.008)
        time.sleep(0.15)

    print("\n[Retrieved Cards]")
    for i, chunk in enumerate(bundle.chunks, 1):
        wrapped = textwrap.fill(chunk.text, width=72, subsequent_indent="      ")
        print(f"{i}. {chunk.source}  (score={chunk.score:.3f})")
        print(f"   {wrapped}")

    print("\n[Final Answer]")
    print(textwrap.fill(bundle.answer, width=76))

    print("\n[Why this matters]")
    print("- You can see the RAG lifecycle before touching model infra.")
    print("- You can teach the concept live in under two minutes.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Polished mock trace demo")
    # Custom prompt for live demos/classes.
    parser.add_argument(
        "--question",
        default="Why does chunking help a RAG system answer better?",
        help="Question to demonstrate",
    )
    # Shared visualization behavior across scripts.
    parser.add_argument(
        "--visualize",
        choices=["auto", "popup", "terminal", "off"],
        default="auto",
        help="Display mode: auto popup, forced popup, terminal, or off",
    )
    args = parser.parse_args()
    run_demo(args.question, args.visualize)
