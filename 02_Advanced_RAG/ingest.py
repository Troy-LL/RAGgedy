import os
import pickle
import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from rank_bm25 import BM25Okapi
from sentence_transformers import CrossEncoder

import config

def main():
    print("Starting 02_Advanced_RAG Ingestion...")
    
    cfg = config.CONFIG
    
    # Ensure directories exist
    os.makedirs(cfg["passages_dir"], exist_ok=True)
    os.makedirs(cfg["chroma_db_path"], exist_ok=True)
    os.makedirs(cfg["bm25_index_path"], exist_ok=True)

    # 1. Load Documents
    print(f"Loading documents from {cfg['passages_dir']}...")
    documents = SimpleDirectoryReader(cfg['passages_dir']).load_data()
    print(f"Loaded {len(documents)} documents.")
    
    if len(documents) == 0:
        print("No documents found. Please supply synthetic data!")
        return

    # 2. Chunking
    print(f"Chunking with size={cfg['chunk_size']}, overlap={cfg['chunk_overlap']}...")
    parser = SentenceSplitter(chunk_size=cfg['chunk_size'], chunk_overlap=cfg['chunk_overlap'])
    nodes = parser.get_nodes_from_documents(documents)
    print(f"Created {len(nodes)} chunks.")

    # 3. Embedding Model
    print(f"Loading embedding model: {cfg['embedding_model']}")
    embed_model = HuggingFaceEmbedding(model_name=cfg['embedding_model'])

    # 4. Vector DB Setup (Semantic)
    print(f"Initializing ChromaDB at {cfg['chroma_db_path']}...")
    db = chromadb.PersistentClient(path=cfg['chroma_db_path'])
    chroma_collection = db.get_or_create_collection("advanced_rag_collection")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # 5. Build and Persist Index (Semantic)
    print("Building semantic index and embedding chunks (this might take a few minutes)...")
    index = VectorStoreIndex(
        nodes,
        storage_context=storage_context,
        embed_model=embed_model,
        show_progress=True
    )
    
    # 6. Build BM25 Index (Sparse)
    print("Building BM25 sparse index...")
    # Extract text from nodes for BM25
    corpus_texts = [node.get_content() for node in nodes]
    corpus_tokenized = [text.lower().split() for text in corpus_texts]
    bm25 = BM25Okapi(corpus_tokenized)
    
    # Save the BM25 model, along with nodes mappings if necessary
    # We will need the mapping from doc_id or just nodes back to text during query time.
    bm25_data = {
        "bm25": bm25,
        "nodes": nodes  # Store nodes here so we can retrieve full text/metadata later via index.
    }
    
    bm25_file_path = os.path.join(cfg['bm25_index_path'], "bm25_model.pkl")
    with open(bm25_file_path, "wb") as f:
        pickle.dump(bm25_data, f)
    
    # 7. Initialize Reranker Model
    if cfg['reranker_enabled']:
        print(f"Loading cross-encoder reranker model: {cfg['reranker_model']} (will cache locally)...")
        _ = CrossEncoder(cfg['reranker_model'], max_length=512)

    print("✅ Ingestion complete.")
    print("Vectors persisted to ChromaDB and BM25 index saved.")

if __name__ == "__main__":
    main()
