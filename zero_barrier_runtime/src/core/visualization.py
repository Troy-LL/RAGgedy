from __future__ import annotations

from datetime import datetime
from typing import Any

from .types import AnswerBundle


def format_bundle_text(bundle: AnswerBundle) -> str:
    lines: list[str] = []
    lines.append("=" * 64)
    lines.append(f"Mode: {bundle.mode}")
    lines.append(f"Question: {bundle.question}")
    lines.append("=" * 64)

    if bundle.trace:
        lines.append("")
        lines.append("Trace")
        for step in bundle.trace:
            lines.append(f"- {step}")

    lines.append("")
    lines.append("Retrieved Context")
    if bundle.chunks:
        for idx, chunk in enumerate(bundle.chunks, start=1):
            lines.append(f"[{idx}] {chunk.source} | score={chunk.score:.3f}")
            lines.append(f"    {chunk.text}")
    else:
        lines.append("(No retrieved chunks)")

    lines.append("")
    lines.append("Final Answer")
    lines.append(bundle.answer)
    lines.append("")
    lines.append(f"Latency: {bundle.metadata.get('latency_ms', '?')} ms")
    lines.append(f"Rendered at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return "\n".join(lines)


def try_show_popup(bundle: AnswerBundle) -> bool:
    return try_show_popup_text(
        title="RAGgedy Runtime Visualization",
        body=format_bundle_text(bundle),
        header=f"Mode: {bundle.mode} | Top-K: {bundle.metadata.get('top_k', '?')}",
    )


def try_show_popup_text(title: str, body: str, header: str | None = None) -> bool:
    try:
        import tkinter as tk
        from tkinter import scrolledtext
    except Exception:
        return False

    try:
        root = tk.Tk()
        root.title(title)
        root.geometry("980x700")

        if header:
            header_label = tk.Label(
                root,
                text=header,
                anchor="w",
                padx=10,
                pady=8,
            )
            header_label.pack(fill="x")

        area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas", 10))
        area.insert(tk.END, body)
        area.configure(state="disabled")
        area.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        root.mainloop()
        return True
    except Exception:
        return False


def render_text(text: str, visualize_mode: str, *, title: str, header: str | None = None) -> None:
    if visualize_mode == "off":
        return

    if visualize_mode == "terminal":
        print(text)
        return

    if visualize_mode in {"auto", "popup"}:
        shown = try_show_popup_text(title=title, body=text, header=header)
        if shown:
            return
        if visualize_mode == "popup":
            print("Popup visualization unavailable on this environment; falling back to terminal output.")

    print(text)
