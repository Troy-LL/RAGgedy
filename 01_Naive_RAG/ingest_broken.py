import os
import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import config

# Degraded Settings
BROKEN_COLLECTION_NAME = f"{config.DATASET_ID}_broken"
BROKEN_CHUNK_SIZE = 4096
BROKEN_CHUNK_OVERLAP = 0

def main():
    print("Starting 01_Naive_RAG Ingestion (BROKEN VARIANT)...")

    os.makedirs(config.PASSAGES_DIR, exist_ok=True)
    os.makedirs(config.CHROMA_DIR, exist_ok=True)

    # 1. Load Documents
    print("Loading documents...")
    documents = SimpleDirectoryReader(config.PASSAGES_DIR).load_data()
    print(f"Loaded {len(documents)} documents.")

    if len(documents) == 0:
        print("No documents found. Please run generate_datasets.py first!")
        return

    # 2. Broken Chunking
    print(f"Using BROKEN chunking: size={BROKEN_CHUNK_SIZE}, overlap={BROKEN_CHUNK_OVERLAP}...")
    parser = SentenceSplitter(chunk_size=BROKEN_CHUNK_SIZE, chunk_overlap=BROKEN_CHUNK_OVERLAP)
    nodes = parser.get_nodes_from_documents(documents)
    print(f"Created {len(nodes)} extremely large chunks (context will be blurred).")

    # 3. Embedding Model
    print(f"Loading embedding model: {config.EMBED_MODEL}")
    embed_model = HuggingFaceEmbedding(model_name=config.EMBED_MODEL)

    # 4. Broken Vector DB Setup
    print(f"Initializing separate broken collection at {config.CHROMA_DIR}...")
    db = chromadb.PersistentClient(path=config.CHROMA_DIR)
    chroma_collection = db.get_or_create_collection(BROKEN_COLLECTION_NAME)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # 5. Build and Persist Index
    print("Building degraded index and embedding broken chunks...")
    index = VectorStoreIndex(
        nodes,
        storage_context=storage_context,
        embed_model=embed_model,
        show_progress=True
    )

    print("❌ Broken Ingestion complete.")
    print("Run `evaluation/eval_naive.py` to see how severely these poor settings affect the Ragas scores.")

if __name__ == "__main__":
    main()
