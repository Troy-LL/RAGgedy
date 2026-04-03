import textwrap
import time

from zero_barrier_runtime.src.modes.mock_mode import build_mock_orchestrator


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


def run_demo(question: str):
    print(HEADER)
    print()
    type_line(f"Learner asks: {question}", delay=0.01)
    time.sleep(0.2)

    orchestrator = build_mock_orchestrator()
    bundle = orchestrator.ask(question, top_k=3, include_trace=True)

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
    run_demo("Why does chunking help a RAG system answer better?")
