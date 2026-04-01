import os
import sys
import chromadb
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
import config

def main():
    print("Loading 01_Naive_RAG Query Engine...")

    # Configure Global Settings
    Settings.llm = Ollama(model=config.LLM_MODEL, base_url=config.LLM_BASE_URL)
    Settings.embed_model = HuggingFaceEmbedding(model_name=config.EMBED_MODEL)
    
    # Load Vector DB
    try:
        db = chromadb.PersistentClient(path=config.CHROMA_DIR)
        chroma_collection = db.get_collection(config.COLLECTION_NAME)
    except Exception as e:
        print(f"Error: Could not load ChromaDB index from {config.CHROMA_DIR}. Did you run `python ingest.py` first?")
        sys.exit(1)

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    # Reconstruct Index
    index = VectorStoreIndex.from_vector_store(
        vector_store,
        storage_context=storage_context
    )
    
    # Setup Query Engine
    query_engine = index.as_query_engine(similarity_top_k=config.TOP_K)
    
    print("\n" + "="*50)
    print("🤖 Edu-Scholar RAG Ready!")
    print("Type your questions below. Enter 'quit' or 'exit' to leave.")
    print("="*50)

    while True:
        try:
            user_input = input("\nQuery > ")
            if user_input.lower().strip() in ["quit", "exit"]:
                print("Goodbye!")
                break
                
            if not user_input.strip():
                continue
                
            print("Thinking...")
            response = query_engine.query(user_input)
            
            print("\n" + "="*10 + " ANSWER " + "="*10)
            print(str(response).strip())
            
            print("\n" + "="*10 + " SOURCES " + "="*9)
            for idx, source_node in enumerate(response.source_nodes, 1):
                score = source_node.score
                content = source_node.node.get_content().replace('\n', ' ')
                snippet = content[:80] + "..." if len(content) > 80 else content
                filename = source_node.node.metadata.get('file_name', 'Unknown')
                print(f"[{idx}] {filename} (Score: {score:.4f}) -> {snippet}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
