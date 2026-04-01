# RAGgedy 🧩

**RAGgedy** is an open-source educational repository of Retrieval-Augmented Generation (RAG) templates, designed as a modular "Lego kit" for developers. 

Most RAG examples are monolithic. **RAGgedy** breaks the RAG pipeline into distinct, clear, and modular stages, starting from first principles and increasing in complexity across successive modules.

---

## 🏗️ Project Architecture

RAGgedy is organized into numbered modules, each focusing on a specific architectural shift or technique.

### 01_Naive_RAG (Current Module)
- **Goal**: Build the simplest functional RAG pipeline with zero proprietary dependencies.
- **Tech Stack**: [LlamaIndex](https://www.llamaindex.ai/), [Ollama](https://ollama.com/) (llama3), [BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3) embeddings, [ChromaDB](https://www.trychroma.com/).
- **Dataset**: *Edu-Scholar* — A purpose-built, synthetic student-tutor dataset for CET preparation.

---

## 🚀 Quick Start

Ensure you have [Ollama](https://ollama.com/) installed and running locally.

### 1. Pull the Model
```bash
ollama pull llama3
```

### 2. Environment Setup
```bash
# Clone the repository
git clone https://github.com/Troy-LL/RAGgedy.git
cd RAGgedy

# Create a virtual environment
python -m venv .venv
# Activate (Windows)
.venv\Scripts\activate
# Activate (Linux/Mac)
source .venv/bin/activate

# Install dependencies
pip install -r 01_Naive_RAG/requirements.txt
```

### 3. Run the Pipeline
```bash
cd 01_Naive_RAG

# Build the vector index
python ingest.py

# Query the pipeline
python query.py
```

---

## 🛠️ Module Roadmap

- [x] **01_Naive_RAG**: The entry-point pipeline with Good/Broken variants.
- [ ] **02_Advanced_RAG**: Hybrid search (BM25), reranking, and HyDE.
- [ ] **03_Agentic_RAG**: Self-correction, tool use, and multi-step reasoning.
- [ ] **04_Geo_RAG**: Spatial-semantic indexing for geographic queries.

---

## 🧪 Evaluation

RAGgedy uses [Ragas](https://docs.ragas.io/en/stable/) for objective pipeline evaluation. We target `Faithfulness >= 0.55` and `Context Precision >= 0.60` for the naive baseline.

---

## ⚖️ License

MIT License. See [LICENSE](LICENSE) for more details.
