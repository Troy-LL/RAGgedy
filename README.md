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

## 🗺️ Pick Your Path (Zero-Barrier)

```mermaid
flowchart LR
	Q["How do you want to learn?"] --> A{"Your setup"}
	A -->|"No API, no model"| T1["Tier 1: Theoretical Sandbox"]
	A -->|"Internet + API key"| T2["Tier 2: Cloud Pilot"]
	A -->|"Local runtime + privacy"| T3["Tier 3: Local Titan"]

	T1 --> T1a["Simulated Thoughts -> Actions -> Results"]
	T2 --> T2a["Hosted OSS models: Groq/Together/HF"]
	T3 --> T3a["Ollama/local execution"]

	classDef q fill:#f8fafc,stroke:#334155,color:#0f172a;
	classDef t1 fill:#fef3c7,stroke:#a16207,color:#422006;
	classDef t2 fill:#dbeafe,stroke:#1d4ed8,color:#0f172a;
	classDef t3 fill:#dcfce7,stroke:#166534,color:#052e16;
	class Q,A q;
	class T1,T1a t1;
	class T2,T2a t2;
	class T3,T3a t3;
```

### Start in under 2 minutes

```bash
python -m zero_barrier_runtime.app --mode mock --question "Why does chunking help?" --show-trace
python -m zero_barrier_runtime.scripts.mock_trace_demo
```

Design docs for the zero-barrier model:

- [docs/zero_barrier/README_TEMPLATE.md](docs/zero_barrier/README_TEMPLATE.md)
- [docs/zero_barrier/CODE_STRUCTURE_PLAN.md](docs/zero_barrier/CODE_STRUCTURE_PLAN.md)
- [docs/zero_barrier/TUTORIAL_ELI5.md](docs/zero_barrier/TUTORIAL_ELI5.md)

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

| Module | What you learn | Run docs |
|---|---|---|
| 01_Naive_RAG | Baseline chunk -> embed -> retrieve -> generate | [01_Naive_RAG/README.md](01_Naive_RAG/README.md) |
| 02_Advanced_RAG | Hybrid retrieval (dense + BM25), RRF, rerank | [02_Advanced_RAG/README.md](02_Advanced_RAG/README.md) |

```mermaid
flowchart LR
	M1[01 Naive RAG] --> M2[02 Advanced RAG]
	M2 --> M3[03 Agentic RAG - planned]
	M3 --> M4[04 Geo RAG - planned]

	classDef done fill:#dcfce7,stroke:#166534,color:#052e16;
	classDef plan fill:#e2e8f0,stroke:#475569,color:#0f172a;
	class M1,M2 done;
	class M3,M4 plan;
```

---

## 🚀 Quick Start

### 1) Setup

```bash
git clone https://github.com/Troy-LL/RAGgedy.git
cd RAGgedy
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r 01_Naive_RAG/requirements.txt
pip install -r 02_Advanced_RAG/requirements.txt
```

### 3) Run baseline module

```bash
cd 01_Naive_RAG
python ingest.py
python query.py
```

### 4) Run advanced module

```bash
cd 02_Advanced_RAG
python ingest.py
python query.py
```

### 5) Optional visualization app

```bash
pip install -r visualization/requirements.txt
streamlit run visualization/app.py
```

See [visualization/README.md](visualization/README.md) for stage-by-stage UI behavior.

---

## 🧪 Evaluation Targets

| Module | Faithfulness | Context Precision |
|---|---:|---:|
| 01_Naive_RAG | 0.55+ | 0.60+ |
| 02_Advanced_RAG | 0.65+ | 0.72+ |

Run:

```bash
python 01_Naive_RAG/evaluation/eval_naive.py
python 02_Advanced_RAG/evaluation/eval_advanced.py
```

---

## 🧠 Why This Repo Feels Different

- Learning-first: every module is runnable and intentionally scoped.
- Compare-forward: good vs broken variants show failure modes clearly.
- Zero-barrier: mock, cloud, and local paths support different hardware realities.

---

## ⚖️ License

[LICENSE](LICENSE) (MIT)
