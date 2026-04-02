import os
import sys
import chromadb
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama


def load_naive_query_engine(config_mod=None):
    """Load the naive RAG query engine. Pass a loaded `config` module (e.g. from importlib) when not using default env."""
    if config_mod is None:
        import config as config_mod

    Settings.llm = Ollama(model=config_mod.LLM_MODEL, base_url=config_mod.LLM_BASE_URL)
    Settings.embed_model = HuggingFaceEmbedding(model_name=config_mod.EMBED_MODEL)

    try:
        db = chromadb.PersistentClient(path=config_mod.CHROMA_DIR)
        chroma_collection = db.get_collection(config_mod.COLLECTION_NAME)
    except Exception as e:
        raise RuntimeError(
            f"Could not load ChromaDB index from {config_mod.CHROMA_DIR}. "
            "Did you run `python ingest.py` first?"
        ) from e

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)
    return index.as_query_engine(similarity_top_k=config_mod.TOP_K)


def run_naive_query(query_engine, user_input):
    """Run one query; return answer text and source metadata for UIs."""
    response = query_engine.query(user_input)
    sources = []
    for sn in response.source_nodes:
        content = sn.node.get_content().replace("\n", " ")
        sources.append(
            {
                "filename": sn.node.metadata.get("file_name", "Unknown"),
                "score": sn.score,
                "snippet": content[:200] + ("..." if len(content) > 200 else ""),
            }
        )
    return {"answer": str(response).strip(), "sources": sources}


def main():
    print("Loading 01_Naive_RAG Query Engine...")
    import config

    try:
        query_engine = load_naive_query_engine(config)
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print("\n" + "=" * 50)
    print("🤖 Edu-Scholar RAG Ready!")
    print("Type your questions below. Enter 'quit' or 'exit' to leave.")
    print("=" * 50)

    while True:
        try:
            user_input = input("\nQuery > ")
            if user_input.lower().strip() in ["quit", "exit"]:
                print("Goodbye!")
                break

            if not user_input.strip():
                continue

            print("Thinking...")
            out = run_naive_query(query_engine, user_input)

            print("\n" + "=" * 10 + " ANSWER " + "=" * 10)
            print(out["answer"])

            print("\n" + "=" * 10 + " SOURCES " + "=" * 9)
            for idx, s in enumerate(out["sources"], 1):
                snip = s["snippet"].replace("\n", " ")
                short = snip[:80] + "..." if len(snip) > 80 else snip
                print(f"[{idx}] {s['filename']} (Score: {s['score']:.4f}) -> {short}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
