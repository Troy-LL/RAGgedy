import os

# Centralized configuration for 02_Advanced_RAG
CONFIG = {
    # === DATA ===
    "data_dir": "data/",
    "passages_dir": "data/passages/",
    "questions_file": "data/questions.json",
    "chroma_db_path": ".chroma/",
    "bm25_index_path": ".bm25_index/",  # Persisted BM25 index
    
    # === CHUNKING ===
    "chunk_size": 512,
    "chunk_overlap": 64,
    "splitter": "sentence",
    
    # === EMBEDDINGS ===
    "embedding_model": "BAAI/bge-m3",
    "device": "cpu",
    
    # === VECTOR DB ===
    "vector_db": "chromadb",
    "vector_db_path": ".chroma/",
    
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

# Create necessary directories
os.makedirs(CONFIG["chroma_db_path"], exist_ok=True)
os.makedirs(CONFIG["bm25_index_path"], exist_ok=True)
