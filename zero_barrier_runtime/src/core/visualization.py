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
    stages = _default_stages_for_bundle(bundle)
    return try_show_graph_popup_text(
        title="RAGgedy Runtime Visualization",
        body=format_bundle_text(bundle),
        header=f"Mode: {bundle.mode} | Top-K: {bundle.metadata.get('top_k', '?')}",
        stages=stages,
        edge_descriptions=_bundle_edge_descriptions(bundle, stages),
        stage_descriptions=_default_stage_descriptions(stages),
        component_lines=_bundle_component_lines(bundle),
    )


def try_show_popup_text(title: str, body: str, header: str | None = None) -> bool:
    # Backward-compatible wrapper used by older call sites.
    return try_show_graph_popup_text(title=title, body=body, header=header)


def _default_stages_for_bundle(bundle: AnswerBundle) -> list[str]:
    if bundle.mode == "mock":
        return ["Question", "Retrieve", "Ground", "Generate", "Response"]
    return ["Question", "Retrieve", "Context", "Generate", "Response"]


def _default_stage_descriptions(stages: list[str]) -> list[str]:
    mapping = {
        "Question": "User input enters the pipeline and intent is interpreted.",
        "Retrieve": "Retriever searches indexed chunks and ranks likely matches.",
        "Ground": "Retrieved chunks are validated/organized as grounded evidence.",
        "Context": "Selected chunks are assembled into the model context block.",
        "Generate": "LLM generates an answer constrained by retrieved evidence.",
        "Response": "Final answer is returned with supporting context details.",
    }
    return [mapping.get(stage, "Pipeline stage") for stage in stages]


def _bundle_edge_descriptions(bundle: AnswerBundle, stages: list[str]) -> list[str]:
    source_names = [c.source for c in bundle.chunks[:3]]
    sources_preview = ", ".join(source_names) if source_names else "no chunks found"
    top_k = bundle.metadata.get("top_k", len(bundle.chunks))

    descriptions = [
        "Question is parsed into retrieval intent and key terms.",
        f"Retriever queries the index and pulls top-{top_k} chunks: {sources_preview}.",
        "Retrieved evidence is filtered and grounded into a coherent context window.",
        "LLM uses grounded context to compose an answer with lower hallucination risk.",
    ]

    needed = max(1, len(stages) - 1)
    if len(descriptions) < needed:
        descriptions.extend(["Transition to next stage."] * (needed - len(descriptions)))
    return descriptions[:needed]


def _bundle_component_lines(bundle: AnswerBundle) -> list[str]:
    retrieved = len(bundle.chunks)
    top_k = bundle.metadata.get("top_k", retrieved)
    latency = bundle.metadata.get("latency_ms", "?")
    first = bundle.chunks[0].source if bundle.chunks else "none"
    return [
        f"Mode: {bundle.mode}",
        f"Top-K configured: {top_k}",
        f"Retrieved chunks: {retrieved}",
        f"Latency: {latency} ms",
        f"Top source: {first}",
    ]


def _edge_midpoint(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return ((a[0] + b[0]) // 2, (a[1] + b[1]) // 2)


def _point_on_segment(a: tuple[int, int], b: tuple[int, int], t: float) -> tuple[int, int]:
    x = int(a[0] + (b[0] - a[0]) * t)
    y = int(a[1] + (b[1] - a[1]) * t)
    return x, y


def _draw_graph(canvas: Any, stages: list[str], active_edge: int, dot_t: float) -> None:
    canvas.delete("all")
    width = int(canvas["width"])
    y = 170
    left = 80
    spacing = max(120, (width - 2 * left) // max(1, len(stages) - 1))

    nodes: list[tuple[int, int]] = []
    for idx, stage in enumerate(stages):
        x = left + idx * spacing
        nodes.append((x, y))
        fill = "#dce8f7" if idx <= active_edge + 1 else "#f2f2f2"
        outline = "#4f6b8f" if idx <= active_edge + 1 else "#777777"
        canvas.create_rectangle(x - 60, y - 30, x + 60, y + 30, fill=fill, outline=outline, width=2)
        canvas.create_text(x, y, text=stage, font=("Segoe UI", 10, "bold"))

    for edge_idx in range(len(nodes) - 1):
        a = nodes[edge_idx]
        b = nodes[edge_idx + 1]
        color = "#3f3f3f"
        width_px = 3
        if edge_idx == active_edge:
            color = "#1f78ff"
            width_px = 4
        canvas.create_line(a[0] + 62, a[1], b[0] - 62, b[1], arrow="last", fill=color, width=width_px)

        mx, my = _edge_midpoint((a[0] + 62, a[1]), (b[0] - 62, b[1]))
        canvas.create_oval(mx - 12, my - 12, mx + 12, my + 12, fill="#ff9d2f", outline="#8a4f00", width=1)
        canvas.create_text(mx, my, text=str(edge_idx + 1), font=("Segoe UI", 9, "bold"))

        if edge_idx == active_edge:
            dx, dy = _point_on_segment((a[0] + 62, a[1]), (b[0] - 62, b[1]), dot_t)
            canvas.create_oval(dx - 6, dy - 6, dx + 6, dy + 6, fill="#00c853", outline="#0f5f32", width=1)

    canvas.create_text(
        width // 2,
        35,
        text="Pipeline Graph (animated dot shows current process step)",
        font=("Segoe UI", 11),
    )


def _draw_architecture(canvas: Any, component_lines: list[str], active_edge: int, dot_t: float) -> None:
    canvas.delete("all")
    width = int(canvas["width"])
    height = int(canvas["height"])
    sx = width / 1060.0
    sy = height / 360.0

    def _pt(x: int, y: int) -> tuple[int, int]:
        return int(x * sx), int(y * sy)

    def _rect(r: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
        x1, y1, x2, y2 = r
        p1 = _pt(x1, y1)
        p2 = _pt(x2, y2)
        return p1[0], p1[1], p2[0], p2[1]

    canvas.create_text(
        width // 2,
        int(20 * sy),
        text="RAG Components Diagram",
        font=("Segoe UI", 11),
    )

    # Top lane: Documents -> Embeddings -> Vector DB <- Prompt Embedding
    docs = _rect((110, 92, 220, 152))
    embed = _rect((300, 80, 470, 165))
    vdb = _rect((580, 70, 700, 182))
    prompt_emb = _rect((790, 92, 980, 152))

    # Bottom lane: Prompt -> Prompt+Context -> LLM -> Result
    prompt = _rect((80, 245, 190, 305))
    prompt_ctx = _rect((260, 225, 460, 325))
    llm = _rect((540, 225, 700, 325))
    result = _rect((800, 238, 900, 312))

    # Node drawing helpers
    def box(rect: tuple[int, int, int, int], text: str, fill: str = "#eef3fa") -> None:
        x1, y1, x2, y2 = rect
        canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="#4f6b8f", width=2)
        canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=text, font=("Segoe UI", 10, "bold"))

    def arrow(p1: tuple[int, int], p2: tuple[int, int], text: str | None = None) -> None:
        canvas.create_line(p1[0], p1[1], p2[0], p2[1], arrow="last", fill="#3f3f3f", width=2)
        if text:
            mx = (p1[0] + p2[0]) // 2
            my = (p1[1] + p2[1]) // 2 - 10
            canvas.create_text(mx, my, text=text, font=("Segoe UI", 9))

    box(docs, "Documents")
    box(embed, "Generate\nEmbeddings")
    box(prompt_emb, "Prompt\nEmbedding")
    box(prompt, "Prompt")
    box(prompt_ctx, "Prompt\n+\nContext")
    box(llm, "LLM", fill="#dce8f7")
    box(result, "Result", fill="#f5f5f5")

    # Approximate DB cylinder
    x1, y1, x2, y2 = vdb
    canvas.create_oval(x1, y1, x2, y1 + 30, fill="#e9eef7", outline="#4f6b8f", width=2)
    canvas.create_rectangle(x1, y1 + 15, x2, y2 - 15, fill="#e9eef7", outline="#4f6b8f", width=2)
    canvas.create_oval(x1, y2 - 30, x2, y2, fill="#d7e2f2", outline="#4f6b8f", width=2)
    canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text="Vector DB", font=("Segoe UI", 10, "bold"))

    y_mid_top = _pt(0, 122)[1]
    y_mid_bottom = _pt(0, 275)[1]
    arrow((docs[2], y_mid_top), (embed[0], y_mid_top), "Chunked Texts")
    arrow((embed[2], y_mid_top), (vdb[0], y_mid_top), "Embeddings")
    arrow((prompt_emb[0], y_mid_top), (vdb[2], y_mid_top), "Prompt Embedding")
    arrow((vdb[0] + int(40 * sx), vdb[3]), (prompt_ctx[0] + int(30 * sx), prompt_ctx[1]), "Most relevant passages")
    arrow((prompt[2], y_mid_bottom), (prompt_ctx[0], y_mid_bottom))
    arrow((prompt_ctx[2], y_mid_bottom), (llm[0], y_mid_bottom))
    arrow((llm[2], y_mid_bottom), (result[0], y_mid_bottom))

    # Animated dot around key transition groups to indicate active system phase.
    phase_edges = [
        ((docs[2], y_mid_top), (embed[0], y_mid_top)),
        ((embed[2], y_mid_top), (vdb[0], y_mid_top)),
        ((vdb[0] + int(40 * sx), vdb[3]), (prompt_ctx[0] + int(30 * sx), prompt_ctx[1])),
        ((prompt_ctx[2], y_mid_bottom), (llm[0], y_mid_bottom)),
        ((llm[2], y_mid_bottom), (result[0], y_mid_bottom)),
    ]
    phase_idx = active_edge % len(phase_edges)
    p1, p2 = phase_edges[phase_idx]
    dx, dy = _point_on_segment(p1, p2, dot_t)
    canvas.create_oval(dx - 7, dy - 7, dx + 7, dy + 7, fill="#00c853", outline="#0f5f32", width=1)

    # Characteristics block.
    canvas.create_rectangle(_pt(12, 12)[0], _pt(12, 12)[1], _pt(250, 170)[0], _pt(250, 170)[1], fill="#fff9ed", outline="#c79a4b", width=1)
    canvas.create_text(_pt(22, 28)[0], _pt(22, 28)[1], anchor="w", text="Characteristics", font=("Segoe UI", 9, "bold"))
    for idx, line in enumerate(component_lines[:6]):
        p = _pt(22, 48 + idx * 18)
        canvas.create_text(p[0], p[1], anchor="w", text=f"- {line}", font=("Segoe UI", 9))


def _build_answer_key(stages: list[str], edge_descriptions: list[str]) -> str:
    lines = ["Correct Sequence / Answer Key", ""]
    for i, stage in enumerate(stages, 1):
        lines.append(f"{i}. {stage}")
    lines.append("")
    lines.append("Expected transitions")
    for i, desc in enumerate(edge_descriptions, 1):
        lines.append(f"{i}. {desc}")
    lines.append("")
    lines.append("Use this as the target flow when validating runs.")
    return "\n".join(lines)


def try_show_graph_popup_text(
    title: str,
    body: str,
    header: str | None = None,
    stages: list[str] | None = None,
    edge_descriptions: list[str] | None = None,
    stage_descriptions: list[str] | None = None,
    component_lines: list[str] | None = None,
) -> bool:
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox, scrolledtext
    except Exception:
        return False

    if not stages:
        stages = ["Question", "Retrieve", "Context", "Generate", "Response"]
    edge_count = max(1, len(stages) - 1)

    if edge_descriptions is None:
        edge_descriptions = [
            "Question is interpreted and prepared for retrieval.",
            "Retriever searches vector/sparse indexes and picks top evidence.",
            "Evidence is packaged into model-ready context.",
            "LLM generates grounded output for the final response.",
        ]
    if len(edge_descriptions) < edge_count:
        edge_descriptions = edge_descriptions + ["Transition to next stage."] * (
            edge_count - len(edge_descriptions)
        )
    edge_descriptions = edge_descriptions[:edge_count]

    if stage_descriptions is None:
        stage_descriptions = _default_stage_descriptions(stages)
    if len(stage_descriptions) < len(stages):
        stage_descriptions = stage_descriptions + ["Pipeline stage"] * (
            len(stages) - len(stage_descriptions)
        )
    stage_descriptions = stage_descriptions[: len(stages)]

    if component_lines is None:
        component_lines = [
            "Vector retrieval over embedded chunks",
            "Prompt is grounded with retrieved context",
            "LLM generates final response",
        ]

    try:
        root = tk.Tk()
        root.title(title)
        root.geometry("1420x920")

        if header:
            header_label = tk.Label(
                root,
                text=header,
                anchor="w",
                padx=10,
                pady=8,
                font=("Segoe UI", 10, "bold"),
            )
            header_label.pack(fill="x")

        main = tk.Frame(root)
        main.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        left_panel = tk.Frame(main)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 8))
        right_panel = tk.Frame(main)
        right_panel.pack(side="left", fill="both", expand=True, padx=(8, 0))

        graph = tk.Canvas(left_panel, width=760, height=250, bg="#f8f8f8", highlightthickness=1)
        graph.pack(fill="x", pady=(0, 8))

        architecture = tk.Canvas(left_panel, width=760, height=330, bg="#fbfbfb", highlightthickness=1)
        architecture.pack(fill="x", pady=(0, 8))

        controls = tk.Frame(left_panel)
        controls.pack(fill="x", pady=(0, 8))

        explain_frame = tk.Frame(left_panel)
        explain_frame.pack(fill="x", pady=(0, 8))

        left = tk.Frame(explain_frame, bd=1, relief="solid")
        left.pack(side="left", fill="both", expand=True, padx=(0, 6))
        right = tk.Frame(explain_frame, bd=1, relief="solid")
        right.pack(side="left", fill="both", expand=True, padx=(6, 0))

        step_title = tk.Label(left, text="Current Step", anchor="w", padx=8, pady=6, font=("Segoe UI", 10, "bold"))
        step_title.pack(fill="x")
        step_text = tk.Label(left, text="", justify="left", anchor="w", wraplength=500, padx=8, pady=6)
        step_text.pack(fill="x")

        guide_title = tk.Label(right, text="Stage Guide", anchor="w", padx=8, pady=6, font=("Segoe UI", 10, "bold"))
        guide_title.pack(fill="x")
        guide_lines = [f"- {stages[i]}: {stage_descriptions[i]}" for i in range(len(stages))]
        guide_text = tk.Label(right, text="\n".join(guide_lines), justify="left", anchor="w", wraplength=500, padx=8, pady=6)
        guide_text.pack(fill="x")

        key_label = tk.Label(
            right_panel,
            text=_build_answer_key(stages, edge_descriptions),
            justify="left",
            anchor="w",
            wraplength=560,
            padx=8,
            pady=8,
            bd=1,
            relief="solid",
            font=("Segoe UI", 9),
        )
        key_label.pack(fill="x", pady=(0, 8))

        area = scrolledtext.ScrolledText(right_panel, wrap=tk.WORD, font=("Consolas", 10))
        area.insert(tk.END, body)
        area.configure(state="disabled")
        area.pack(fill="both", expand=True)

        state = {"edge": 0, "t": 0.0, "paused": False}

        pause_btn_text = tk.StringVar(value="Pause")
        status_text = tk.StringVar(value="Ready")

        def _toggle_pause() -> None:
            state["paused"] = not state["paused"]
            pause_btn_text.set("Resume" if state["paused"] else "Pause")

        pause_btn = tk.Button(controls, textvariable=pause_btn_text, command=_toggle_pause)
        pause_btn.pack(side="left")

        def _export_png() -> None:
            save_path = filedialog.asksaveasfilename(
                title="Export visualization as PNG",
                defaultextension=".png",
                filetypes=[("PNG image", "*.png")],
                initialfile="raggedy_visualization.png",
            )
            if not save_path:
                return

            try:
                from PIL import ImageGrab
            except Exception:
                messagebox.showerror(
                    "PNG export unavailable",
                    "PNG export requires Pillow. Install with: pip install pillow",
                )
                status_text.set("Export failed: Pillow not installed")
                return

            try:
                root.update_idletasks()
                x1 = main.winfo_rootx()
                y1 = main.winfo_rooty()
                x2 = x1 + main.winfo_width()
                y2 = y1 + main.winfo_height()
                image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
                image.save(save_path, "PNG")
                status_text.set(f"Exported: {save_path}")
            except Exception as exc:
                messagebox.showerror("Export failed", f"Could not export PNG:\n{exc}")
                status_text.set("Export failed")

        export_btn = tk.Button(controls, text="Export PNG", command=_export_png)
        export_btn.pack(side="left", padx=(8, 0))

        hint_label = tk.Label(
            controls,
            text="Tip: press Space to pause/resume animation",
            anchor="w",
            padx=10,
        )
        hint_label.pack(side="left")

        status_label = tk.Label(controls, textvariable=status_text, anchor="e", padx=10)
        status_label.pack(side="right")

        root.bind("<space>", lambda _event: _toggle_pause())

        def _tick() -> None:
            _draw_graph(graph, stages, state["edge"], state["t"])
            _draw_architecture(architecture, component_lines, state["edge"], state["t"])
            edge = state["edge"]
            src = stages[edge]
            dst = stages[min(edge + 1, len(stages) - 1)]
            step_text.configure(
                text=f"{edge + 1}. {src} -> {dst}\n\n{edge_descriptions[edge]}"
            )

            if not state["paused"]:
                state["t"] += 0.08
                if state["t"] > 1.0:
                    state["t"] = 0.0
                    state["edge"] = (state["edge"] + 1) % edge_count
            root.after(90, _tick)

        _tick()
        root.mainloop()
        return True
    except Exception:
        return False


def render_text(
    text: str,
    visualize_mode: str,
    *,
    title: str,
    header: str | None = None,
    stages: list[str] | None = None,
    edge_descriptions: list[str] | None = None,
    stage_descriptions: list[str] | None = None,
) -> None:
    if visualize_mode == "off":
        return

    if visualize_mode == "terminal":
        print(text)
        return

    if visualize_mode in {"auto", "popup"}:
        shown = try_show_graph_popup_text(
            title=title,
            body=text,
            header=header,
            stages=stages,
            edge_descriptions=edge_descriptions,
            stage_descriptions=stage_descriptions,
        )
        if shown:
            return
        if visualize_mode == "popup":
            print("Popup visualization unavailable on this environment; falling back to terminal output.")

    print(text)
