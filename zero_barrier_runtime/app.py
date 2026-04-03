from zero_barrier_runtime.src.config.mode_registry import build_orchestrator
from zero_barrier_runtime.src.config.settings import build_parser
from zero_barrier_runtime.src.core.visualization import try_show_popup


def _print_result(bundle):
    print("\n" + "=" * 64)
    print(f"Mode: {bundle.mode}")
    print(f"Question: {bundle.question}")
    print("=" * 64)

    if bundle.trace:
        print("\nTrace")
        for step in bundle.trace:
            print(f"- {step}")

    print("\nRetrieved Context")
    for idx, chunk in enumerate(bundle.chunks, start=1):
        print(
            f"[{idx}] {chunk.source} | score={chunk.score:.3f}\n"
            f"    {chunk.text}"
        )

    print("\nFinal Answer")
    print(bundle.answer)
    print(f"\nLatency: {bundle.metadata.get('latency_ms', '?')} ms")


def _present_result(bundle, visualize_mode: str) -> None:
    if visualize_mode == "off":
        return

    if visualize_mode == "terminal":
        _print_result(bundle)
        return

    if visualize_mode in {"auto", "popup"}:
        popup_ok = try_show_popup(bundle)
        if popup_ok:
            return
        if visualize_mode == "popup":
            print("Popup visualization unavailable on this environment; falling back to terminal output.")

    _print_result(bundle)


def main():
    parser = build_parser()
    args = parser.parse_args()

    orchestrator = build_orchestrator(args)
    bundle = orchestrator.ask(
        question=args.question,
        top_k=args.top_k,
        include_trace=args.show_trace or args.mode == "mock",
    )
    _present_result(bundle, args.visualize)


if __name__ == "__main__":
    main()
