import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

DATASET_ID = (os.environ.get("RAGGEDY_DATASET", "edu_scholar") or "edu_scholar").strip()
DATASET_DIR = os.path.join(DATA_DIR, "datasets", DATASET_ID)
PASSAGES_DIR = os.path.join(DATASET_DIR, "passages")
QUESTIONS_FILE = os.path.join(DATASET_DIR, "questions.json")
CHROMA_DIR = os.path.join(BASE_DIR, ".chroma", DATASET_ID)
BM25_DIR = os.path.join(BASE_DIR, ".bm25_index", DATASET_ID)
BROKEN_CHROMA_DIR = os.path.join(BASE_DIR, ".chroma_broken", DATASET_ID)
BROKEN_BM25_DIR = os.path.join(BASE_DIR, ".bm25_broken", DATASET_ID)

# Centralized configuration for 02_Advanced_RAG
CONFIG = {
    # === DATA ===
    "dataset_id": DATASET_ID,
    "data_dir": DATASET_DIR + os.sep,
    "passages_dir": PASSAGES_DIR + os.sep,
    "questions_file": QUESTIONS_FILE,
    "chroma_db_path": CHROMA_DIR + os.sep,
    "bm25_index_path": BM25_DIR + os.sep,
    "broken_chroma_db_path": BROKEN_CHROMA_DIR + os.sep,
    "broken_bm25_index_path": BROKEN_BM25_DIR + os.sep,

    # === CHUNKING ===
    "chunk_size": 512,
    "chunk_overlap": 64,
    "splitter": "sentence",

    # === EMBEDDINGS ===
    "embedding_model": "BAAI/bge-m3",
    "device": "cpu",

    # === VECTOR DB ===
    "vector_db": "chromadb",
    "vector_db_path": CHROMA_DIR + os.sep,

    # === SEMANTIC RETRIEVAL ===
    "semantic_top_k": 10,
    "semantic_similarity_threshold": 0.0,

    # === BM25 RETRIEVAL ===
    "bm25_top_k": 10,
    "bm25_tokenizer": "whitespace",

    # === FUSION ===
    "fusion_method": "rrf",
    "fusion_top_k": 10,

    # === RERANKING ===
    "reranker_enabled": True,
    "reranker_model": "cross-encoder/ms-marco-MiniLM-L-12-v2",
    "reranker_batch_size": 32,
    "reranker_top_k": 5,
    "reranker_score_threshold": 0.0,

    # === LLM ===
    "llm_model": "llama3",
    "ollama_host": "http://localhost:11434",

    # === RAGAS TARGETS ===
    "ragas_faithfulness_target": 0.65,
    "ragas_context_precision_target": 0.72,
}

os.makedirs(CONFIG["chroma_db_path"], exist_ok=True)
os.makedirs(CONFIG["bm25_index_path"], exist_ok=True)
