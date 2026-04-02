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

**Dataset**: *Edu-Scholar* — a synthetic student–tutor passage set for CET-style preparation (shared under each module’s `data/`).

Module-specific commands, config tables, and architecture diagrams live in each folder’s `README.md` (e.g. [01_Naive_RAG/README.md](01_Naive_RAG/README.md), [02_Advanced_RAG/README.md](02_Advanced_RAG/README.md)).

---

## 🚀 Quick Start

Ensure [Ollama](https://ollama.com/) is installed and running locally.

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
