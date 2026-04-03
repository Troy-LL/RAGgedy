# RAGgedy 🧩

<div align="center">

### Open-Source RAG Templates That Start Simple and Scale Clearly

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Actively%20Maintained-brightgreen.svg)
![Beginner Friendly](https://img.shields.io/badge/Beginner-Friendly-orange.svg)
![Offline First](https://img.shields.io/badge/Mode-Offline%20First-informational.svg)

</div>

RAGgedy is a learning-first RAG repo built like Lego blocks: each module isolates one architectural idea so you can see what changed, why it changed, and how quality improves.

---

## 🧭 Start Here

If you want the shortest path into the repo, open these files first:

| What you want | Open this | Why it helps |
|---|---|---|
| Big-picture overview | [docs/zero_barrier/TUTORIAL_ELI5.md](docs/zero_barrier/TUTORIAL_ELI5.md) | Plain-English walkthrough of the whole runtime |
| Runtime design | [docs/zero_barrier/CODE_STRUCTURE_PLAN.md](docs/zero_barrier/CODE_STRUCTURE_PLAN.md) | Shows how the zero-barrier pieces fit together |
| Module 01 | [01_Naive_RAG/README.md](01_Naive_RAG/README.md) | Baseline chunk -> embed -> retrieve -> generate flow |
| Module 02 | [02_Advanced_RAG/README.md](02_Advanced_RAG/README.md) | Hybrid retrieval, RRF, and reranking |
| Live UI | [visualization/README.md](visualization/README.md) | Step-by-step Streamlit view of ingest/query |
| Mock runtime | [zero_barrier_runtime/app.py](zero_barrier_runtime/app.py) | Entry point for mock, API, and local modes |
| Mock demo | [zero_barrier_runtime/scripts/mock_trace_demo.py](zero_barrier_runtime/scripts/mock_trace_demo.py) | Fastest way to see the trace format |

---

## 🏗️ Architecture At A Glance

```mermaid
flowchart LR
	D[Documents] --> C[Chunk]
	C --> E[Embed]
	E --> V[(Vector Store)]
	Q[User Question] --> R[Retrieve]
	V --> R
	R --> P[Prompt With Context]
	P --> L[LLM]
	L --> A[Answer + Sources]

	classDef neutral fill:#f7f7f5,stroke:#4c4c4c,color:#1f1f1f;
	class D,C,E,V,Q,R,P,L,A neutral;
```

---

## 📚 Module Map

| Module | What you learn | Main docs | Run / eval |
|---|---|---|---|
| 01_Naive_RAG | Baseline chunk -> embed -> retrieve -> generate | [README](01_Naive_RAG/README.md), [notebook](01_Naive_RAG/notebooks/01_walkthrough.ipynb) | [ingest](01_Naive_RAG/ingest.py), [query](01_Naive_RAG/query.py), [eval](01_Naive_RAG/evaluation/eval_naive.py) |
| 02_Advanced_RAG | Hybrid retrieval (dense + BM25), RRF, rerank | [README](02_Advanced_RAG/README.md), [notebook](02_Advanced_RAG/notebooks/02_walkthrough.ipynb) | [ingest](02_Advanced_RAG/ingest.py), [query](02_Advanced_RAG/query.py), [eval](02_Advanced_RAG/evaluation/eval_advanced.py) |
| Zero-barrier runtime | Mock, API, and local execution paths | [template](docs/zero_barrier/README_TEMPLATE.md), [tutorial](docs/zero_barrier/TUTORIAL_ELI5.md) | [app](zero_barrier_runtime/app.py), [trace demo](zero_barrier_runtime/scripts/mock_trace_demo.py) |
| Visualization | Live ingest/query stepping | [README](visualization/README.md) | [app](visualization/app.py) |

---

## 🚀 Quick Start

### 1) Set up the environment once

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r 01_Naive_RAG/requirements.txt
pip install -r 02_Advanced_RAG/requirements.txt
pip install -r visualization/requirements.txt
```

### 2) Pick one path

| Path | Best for | Command |
|---|---|---|
| Mock demo | Fastest way to understand the runtime | `python -m zero_barrier_runtime.app --mode mock --question "Why does chunking help?" --show-trace` |
| Trace-only demo | A tiny, no-setup walkthrough | `python -m zero_barrier_runtime.scripts.mock_trace_demo` |
| Module 01 | Classic local-first RAG | `cd 01_Naive_RAG` then `python ingest.py` and `python query.py` |
| Module 02 | Hybrid retrieval and reranking | `cd 02_Advanced_RAG` then `python ingest.py` and `python query.py` |
| Live UI | Step-by-step visual debugging | `streamlit run visualization/app.py` |
| API mode | Hosted OSS models | Set `MODEL_PROVIDER`, `MODEL_NAME`, and `MODEL_API_KEY`, then run `python -m zero_barrier_runtime.app --mode api --question "Explain vector embeddings like I am 5"` |
| Local mode | Private local inference | `ollama pull llama3.1:8b` then `python -m zero_barrier_runtime.app --mode local --local-model llama3.1:8b --question "How does retrieval improve answer quality?"` |

### 3) Follow the deeper paths when you are ready

- [01_Naive_RAG/README.md](01_Naive_RAG/README.md)
- [02_Advanced_RAG/README.md](02_Advanced_RAG/README.md)
- [visualization/README.md](visualization/README.md)
- [docs/zero_barrier/TUTORIAL_ELI5.md](docs/zero_barrier/TUTORIAL_ELI5.md)

---

## 🧪 Evaluation Targets

| Module | Faithfulness | Context Precision | Eval script |
|---|---:|---:|---|
| 01_Naive_RAG | 0.55+ | 0.60+ | [eval_naive.py](01_Naive_RAG/evaluation/eval_naive.py) |
| 02_Advanced_RAG | 0.65+ | 0.72+ | [eval_advanced.py](02_Advanced_RAG/evaluation/eval_advanced.py) |

---

## 🧠 Why This Repo Feels Different

- Learning-first: every module is runnable and intentionally scoped.
- Compare-forward: good vs broken variants show failure modes clearly.
- Zero-barrier: mock, cloud, and local paths support different hardware realities.

---

## ⚖️ License

[LICENSE](LICENSE) (MIT)
