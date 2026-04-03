from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent / "visualization-demo.gif"
W, H = 1280, 620


def _load_font(path: str, size: int):
    try:
        return ImageFont.truetype(path, size=size)
    except Exception:
        return ImageFont.load_default()


FONT_TITLE = _load_font(r"C:\Windows\Fonts\arialbd.ttf", 20)
FONT_BODY = _load_font(r"C:\Windows\Fonts\arial.ttf", 15)
FONT_SMALL = _load_font(r"C:\Windows\Fonts\arial.ttf", 13)
FONT_SMALL_BOLD = _load_font(r"C:\Windows\Fonts\arialbd.ttf", 14)

LEFT = (18, 58, 800, 582)
RIGHT = (820, 58, 1262, 582)

TOP_BOXES = [
    ("Question", (88, 88, 214, 146)),
    ("Retrieve", (258, 88, 384, 146)),
    ("Context", (428, 88, 554, 146)),
    ("LLM", (598, 88, 684, 146)),
]

TOP_ARROWS = [
    ((214, 117), (258, 117)),
    ((384, 117), (428, 117)),
    ((554, 117), (598, 117)),
]

BOTTOM_BOXES = [
    ("Prompt", (92, 392, 220, 454)),
    ("Prompt + Context", (260, 376, 492, 470)),
    ("LLM", (544, 376, 672, 470)),
    ("Result", (710, 388, 784, 450)),
]

BOTTOM_ARROWS = [
    ((220, 423), (260, 423)),
    ((492, 423), (544, 423)),
    ((672, 423), (710, 423)),
]

ANSWER_KEY = ["1. Question", "2. Retrieve", "3. Context", "4. Generate", "5. Response"]
COMPONENT_LINES = [
    "Mode: mock",
    "Top-K configured: 3",
    "Retrieved chunks: 3",
    "Latency: 0.09 ms",
    "Top source: librarian_basics.txt",
]


def lerp(a, b, t):
    return (int(a[0] + (b[0] - a[0]) * t), int(a[1] + (b[1] - a[1]) * t))


def draw_box(draw, rect, label, fill, outline="#4f6b8f", font=FONT_SMALL_BOLD):
    x1, y1, x2, y2 = rect
    draw.rounded_rectangle(rect, radius=14, fill=fill, outline=outline, width=2)
    bbox = draw.textbbox((0, 0), label, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text(((x1 + x2 - tw) / 2, (y1 + y2 - th) / 2), label, fill="black", font=font)


def draw_arrow(draw, p1, p2, color="#3f3f3f", width=3):
    draw.line([p1, p2], fill=color, width=width)
    draw.polygon([(p2[0], p2[1]), (p2[0] - 10, p2[1] - 5), (p2[0] - 10, p2[1] + 5)], fill=color)


frames = []
for i in range(32):
    img = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(img)

    # Titles
    draw.text((24, 12), "RAGgedy Visualization Preview", fill="black", font=FONT_TITLE)
    draw.text((24, 36), "Live animation with dual-lane pipeline, answer key, and details", fill="gray", font=FONT_BODY)

    # Panels
    draw.rounded_rectangle(LEFT, radius=18, fill="#fbfbfb", outline="#d0d0d0")
    draw.rounded_rectangle(RIGHT, radius=18, fill="#ffffff", outline="#d0d0d0")

    # Section titles
    draw.text((86, 60), "Retrieval flow", fill="black", font=FONT_SMALL_BOLD)
    draw.text((86, 300), "Generation flow", fill="black", font=FONT_SMALL_BOLD)
    draw.text((846, 78), "Current Step", fill="black", font=FONT_SMALL_BOLD)
    draw.text((846, 192), "Answer Key", fill="black", font=FONT_SMALL_BOLD)
    draw.text((846, 318), "Characteristics", fill="black", font=FONT_SMALL_BOLD)
    draw.text((846, 474), "Tip", fill="black", font=FONT_SMALL_BOLD)

    # Top lane
    for label, rect in TOP_BOXES:
        fill = "#dce8f7" if label != "Question" else "#e8f0fb"
        draw_box(draw, rect, label, fill, font=FONT_SMALL_BOLD)
    for p1, p2 in TOP_ARROWS:
        draw_arrow(draw, p1, p2)

    for x, y, text in [(262, 62, "Retrieve top passages"), (432, 62, "Assemble context"), (598, 62, "Generate answer")]:
        draw.text((x, y), text, fill="black", font=FONT_SMALL)

    # Bottom lane
    draw.rounded_rectangle((88, 176, 246, 246), radius=12, fill="#fff9ed", outline="#c79a4b", width=2)
    draw.text((100, 186), "Retrieved contexts", fill="black", font=FONT_SMALL_BOLD)
    draw.text((100, 206), "evidence snippets", fill="black", font=FONT_SMALL)
    draw.text((100, 222), "top passages", fill="black", font=FONT_SMALL)

    for label, rect in BOTTOM_BOXES:
        fill = "#f2f2f2" if label == "Prompt" else "#eef3fa"
        if label == "LLM":
            fill = "#dce8f7"
        if label == "Result":
            fill = "#f5f5f5"
        draw_box(draw, rect, label, fill, outline="#6b6b6b" if label == "Prompt" else "#4f6b8f", font=FONT_SMALL_BOLD)
    for p1, p2 in BOTTOM_ARROWS:
        draw_arrow(draw, p1, p2)

    draw.text((88, 322), "Retrieved contexts provide evidence for the answer", fill="black", font=FONT_SMALL)
    draw.text((88, 338), "They are merged with the prompt before the LLM sees them", fill="black", font=FONT_SMALL)

    draw_arrow(draw, (246, 211), (260, 394), color="#c79a4b", width=3)

    # Animated retrieval dot (top lane)
    top_seg = (i // 8) % len(TOP_ARROWS)
    top_t = (i % 8) / 7.0
    top_p = lerp(*TOP_ARROWS[top_seg], top_t)
    draw.ellipse((top_p[0] - 7, top_p[1] - 7, top_p[0] + 7, top_p[1] + 7), fill="#00c853", outline="#0f5f32")

    # Animated generation dot (bottom lane)
    bottom_seg = (i // 8) % len(BOTTOM_ARROWS)
    bottom_t = (i % 8) / 7.0
    bottom_p = lerp(*BOTTOM_ARROWS[bottom_seg], bottom_t)
    draw.ellipse((bottom_p[0] - 6, bottom_p[1] - 6, bottom_p[0] + 6, bottom_p[1] + 6), fill="#ff9d2f", outline="#8a4f00")

    # Right-side live step details
    current_step = [
        ("1. Question -> Retrieve", "Question is converted into retrieval intent."),
        ("2. Retrieve -> Context", "Retriever fetches top passages from the vector store."),
        ("3. Context -> Generate", "Context is assembled from the best passages."),
        ("4. Generate -> Response", "Model generates a grounded response."),
    ][top_seg]
    draw.rounded_rectangle((842, 100, 1240, 168), radius=10, fill="#fff9ed", outline="#c79a4b")
    draw.text((856, 112), current_step[0], fill="black", font=FONT_SMALL_BOLD)
    draw.text((856, 134), current_step[1], fill="black", font=FONT_SMALL)

    draw.rounded_rectangle((842, 214, 1240, 296), radius=10, fill="#f8fbff", outline="#9db7d6")
    for j, line in enumerate(ANSWER_KEY):
        draw.text((856, 226 + j * 14), line, fill="black", font=FONT_SMALL)

    draw.rounded_rectangle((842, 338, 1240, 452), radius=10, fill="#fbfbfb", outline="#cccccc")
    for j, line in enumerate(COMPONENT_LINES):
        draw.text((856, 350 + j * 18), f"- {line}", fill="black", font=FONT_SMALL)

    draw.rounded_rectangle((842, 490, 1240, 532), radius=10, fill="#eef8ef", outline="#9fc59f")
    draw.text((856, 501), "Pause to inspect the graph; export PNG to save it.", fill="black", font=FONT_SMALL)

    frames.append(img)

frames[0].save(OUT, save_all=True, append_images=frames[1:], duration=110, loop=0, disposal=2)
print(OUT)
