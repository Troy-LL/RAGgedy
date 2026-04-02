import os
import pickle
import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

import config

def main():
    print("Starting 02_Advanced_RAG Broken Ingestion...")
    
    cfg = config.CONFIG.copy()
    
    # Degrade configuration (separate broken stores per dataset scenario)
    cfg["chroma_db_path"] = config.CONFIG["broken_chroma_db_path"]
    cfg["bm25_index_path"] = config.CONFIG["broken_bm25_index_path"]
    cfg["chunk_size"] = 1024
    cfg["chunk_overlap"] = 0
    cfg["embedding_model"] = "all-MiniLM-L6-v2" # worse model
    
    # Ensure directories exist
    os.makedirs(cfg["passages_dir"], exist_ok=True)
    os.makedirs(cfg["chroma_db_path"], exist_ok=True)

    # 1. Load Documents
    print(f"Loading documents from {cfg['passages_dir']}...")
    documents = SimpleDirectoryReader(cfg['passages_dir']).load_data()
    print(f"Loaded {len(documents)} documents.")
    
    if len(documents) == 0:
        print("No documents found. Please supply synthetic data!")
        return

    # 2. Chunking (Degraded to 1024 no overlap)
    print(f"Chunking with size={cfg['chunk_size']}, overlap={cfg['chunk_overlap']}...")
    parser = SentenceSplitter(chunk_size=cfg['chunk_size'], chunk_overlap=cfg['chunk_overlap'])
    nodes = parser.get_nodes_from_documents(documents)
    print(f"Created {len(nodes)} chunks.")

    # 3. Embedding Model (Worse)
    print(f"Loading worse embedding model: {cfg['embedding_model']}")
    embed_model = HuggingFaceEmbedding(model_name=cfg['embedding_model'])

    # 4. Vector DB Setup
    print(f"Initializing ChromaDB at {cfg['chroma_db_path']}...")
    db = chromadb.PersistentClient(path=cfg['chroma_db_path'])
    chroma_collection = db.get_or_create_collection("advanced_rag_collection_broken")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # 5. Build and Persist Index
    print("Building degraded index...")
    index = VectorStoreIndex(
        nodes,
        storage_context=storage_context,
        embed_model=embed_model,
        show_progress=True
    )
    
    print("✅ Broken Ingestion complete. Notice we skipped BM25 entirely!")

if __name__ == "__main__":
    main()
