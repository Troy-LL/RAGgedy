# RAGgedy 🧩

**RAGgedy** is an open-source educational repository of Retrieval-Augmented Generation (RAG) templates, designed as a modular "Lego kit" for developers.

Most RAG examples are monolithic. **RAGgedy** breaks the RAG pipeline into distinct, clear, and modular stages, starting from first principles and increasing in complexity across successive modules.

---

## 🏗️ Project Architecture

RAGgedy is organized into numbered modules, each focusing on a specific architectural shift or technique. Each module includes **good** vs **broken** ingestion variants, optional [Ragas](https://docs.ragas.io/en/stable/) evaluation, and a Jupyter walkthrough notebook.

| Module | Focus | Highlights |
|--------|--------|------------|
| **01_Naive_RAG** | Baseline RAG | LlamaIndex, Ollama (llama3), [BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3) embeddings, [ChromaDB](https://www.trychroma.com/), chunk → embed → retrieve → generate |
| **02_Advanced_RAG** | Hybrid retrieval | Dense + [BM25](https://github.com/dorianbrown/rank_bm25) sparse indices, **Reciprocal Rank Fusion (RRF)**, **cross-encoder reranking** (`cross-encoder/ms-marco-MiniLM-L-12-v2`) |

**Datasets**: Each module keeps corpora under `data/datasets/<scenario>/` (default scenario **`edu_scholar`**: synthetic CET-style *Edu-Scholar* passages). Set environment variable **`RAGGEDY_DATASET`** to the scenario folder name to ingest and query a different corpus; indexes are stored per scenario under `.chroma/<scenario>/` (and `.bm25_index/<scenario>/` in module 02). See each module’s `data/README.md`.

Module-specific commands, config tables, and architecture diagrams live in each folder’s `README.md` (e.g. [01_Naive_RAG/README.md](01_Naive_RAG/README.md), [02_Advanced_RAG/README.md](02_Advanced_RAG/README.md)).

---

## 🚀 Quick Start

Ensure [Ollama](https://ollama.com/) is installed and running locally.

---

## 🌈 Zero-Barrier Learning Path

This repository now includes a beginner-first, hardware-flexible documentation pack:

- **Visual README Template**: `docs/zero_barrier/README_TEMPLATE.md`
- **Three-Tier Code Structure Plan**: `docs/zero_barrier/CODE_STRUCTURE_PLAN.md`
- **ELI5 Tutorial Module**: `docs/zero_barrier/TUTORIAL_ELI5.md`

It follows a **Three-Tier Accessibility Model**:

- **Tier 1 — Theoretical Sandbox (Mock Mode)**: Learn instantly with simulated LLM-like traces (no model, no API).
- **Tier 2 — Cloud Pilot (API Mode)**: Use hosted open-source models such as Llama or Mistral through API providers.
- **Tier 3 — Local Titan (On-Prem)**: Run locally for privacy and full control.

Start with the template and adapt module-specific commands as needed.

Quick runnable examples (from repo root):

```bash
python -m zero_barrier_runtime.app --mode mock --question "Why does chunking help?" --show-trace
python -m zero_barrier_runtime.scripts.mock_trace_demo
```

### 1. Pull the chat model

```bash
ollama pull llama3
```

### 2. Environment setup

```bash
git clone https://github.com/Troy-LL/RAGgedy.git
cd RAGgedy

python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate
```

Install dependencies for the module you want to run (each module has its own `requirements.txt`):

```bash
pip install -r 01_Naive_RAG/requirements.txt
# and/or
pip install -r 02_Advanced_RAG/requirements.txt
```

### 3. Run a pipeline

**Naive RAG (Module 01)**

```bash
cd 01_Naive_RAG
python ingest.py
python query.py
```

**Advanced RAG (Module 02)**

```bash
cd 02_Advanced_RAG
python ingest.py
python query.py
```

### 4. Evaluation (optional)

```bash
# From 01_Naive_RAG
python evaluation/eval_naive.py

# From 02_Advanced_RAG
python evaluation/eval_advanced.py
```

### 5. Notebooks

- `01_Naive_RAG/notebooks/01_walkthrough.ipynb`
- `02_Advanced_RAG/notebooks/02_walkthrough.ipynb`

### 6. Live visualization (optional)

Install a module’s `requirements.txt`, then `pip install -r visualization/requirements.txt`. From the repo root:

```bash
streamlit run visualization/app.py
```

The app streams **ingestion** output in real time and shows **query** stages (dense retrieval; for module 02 also BM25, RRF, rerank). See [visualization/README.md](visualization/README.md).

---

## 🛠️ Module Roadmap

- [x] **01_Naive_RAG**: Entry-point pipeline with good/broken variants.
- [x] **02_Advanced_RAG**: Hybrid search (BM25 + dense), RRF fusion, cross-encoder reranking, good/broken variants.
- [ ] **03_Agentic_RAG**: Self-correction, tool use, and multi-step reasoning.
- [ ] **04_Geo_RAG**: Spatial-semantic indexing for geographic queries.

---

## 🧪 Evaluation

RAGgedy uses [Ragas](https://docs.ragas.io/en/stable/) for pipeline evaluation. Reference targets (see each module’s `config` / docs):

- **01_Naive_RAG**: Faithfulness ≥ 0.55, Context precision ≥ 0.60  
- **02_Advanced_RAG**: Faithfulness ≥ 0.65, Context precision ≥ 0.72  

---

## ⚖️ License

MIT License. See [LICENSE](LICENSE) for details.
