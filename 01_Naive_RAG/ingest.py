import os
import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import config

def main():
    print("Starting 01_Naive_RAG Ingestion...")

    # Ensure directories exist
    os.makedirs(config.PASSAGES_DIR, exist_ok=True)
    os.makedirs(config.CHROMA_DIR, exist_ok=True)

    # 1. Load Documents
    print(f"Loading documents from {config.PASSAGES_DIR}...")
    documents = SimpleDirectoryReader(config.PASSAGES_DIR).load_data()
    print(f"Loaded {len(documents)} documents.")
    
    if len(documents) == 0:
        print("No documents found. Please run generate_datasets.py first!")
        return

    # 2. Chunking
    print(f"Chunking with size={config.CHUNK_SIZE}, overlap={config.CHUNK_OVERLAP}...")
    parser = SentenceSplitter(chunk_size=config.CHUNK_SIZE, chunk_overlap=config.CHUNK_OVERLAP)
    nodes = parser.get_nodes_from_documents(documents)
    print(f"Created {len(nodes)} chunks.")

    # 3. Embedding Model
    print(f"Loading embedding model: {config.EMBED_MODEL}")
    embed_model = HuggingFaceEmbedding(model_name=config.EMBED_MODEL)

    # 4. Vector DB Setup
    print(f"Initializing ChromaDB at {config.CHROMA_DIR}...")
    db = chromadb.PersistentClient(path=config.CHROMA_DIR)
    chroma_collection = db.get_or_create_collection(config.COLLECTION_NAME)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # 5. Build and Persist Index
    print("Building index and embedding chunks (this might take a few minutes)...")
    index = VectorStoreIndex(
        nodes,
        storage_context=storage_context,
        embed_model=embed_model,
        show_progress=True
    )

    print("✅ Ingestion complete.")
    print("Vectors persisted to ChromaDB.")
    print("Next step: Run `python query.py` to interact with your data.")

if __name__ == "__main__":
    main()
