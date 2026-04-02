import os
import sys
import pickle
import chromadb
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core.retrievers import VectorIndexRetriever
from sentence_transformers import CrossEncoder


def rrf_fusion(semantic_nodes_with_scores, bm25_nodes_with_scores, k=60):
    fusion_scores = {}
    node_mapping = {}

    for rank, (node, _) in enumerate(semantic_nodes_with_scores):
        if node.node_id not in fusion_scores:
            fusion_scores[node.node_id] = 0
            node_mapping[node.node_id] = node
        fusion_scores[node.node_id] += 1 / (rank + k)

    for rank, (node, _) in enumerate(bm25_nodes_with_scores):
        if node.node_id not in fusion_scores:
            fusion_scores[node.node_id] = 0
            node_mapping[node.node_id] = node
        fusion_scores[node.node_id] += 1 / (rank + k)

    fused = sorted(fusion_scores.items(), key=lambda x: x[1], reverse=True)
    return [(node_mapping[nid], score) for nid, score in fused]


def _node_snippet(node, max_len=200):
    content = node.get_content().replace("\n", " ")
    return content[:max_len] + ("..." if len(content) > max_len else "")


def load_advanced_pipeline(config_mod=None):
    """Load hybrid retriever + BM25 + optional reranker. Pass a loaded `config` module when not using default env."""
    if config_mod is None:
        import config as config_mod

    cfg = config_mod.CONFIG

    Settings.llm = Ollama(
        model=cfg["llm_model"], base_url=cfg["ollama_host"], request_timeout=60.0
    )
    Settings.embed_model = HuggingFaceEmbedding(model_name=cfg["embedding_model"])

    try:
        db = chromadb.PersistentClient(path=cfg["chroma_db_path"])
        chroma_collection = db.get_collection("advanced_rag_collection")
    except Exception as e:
        raise RuntimeError(
            f"Could not load ChromaDB index from {cfg['chroma_db_path']}: {e}"
        ) from e

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)
    semantic_retriever = VectorIndexRetriever(index=index, similarity_top_k=cfg["semantic_top_k"])

    bm25_file_path = os.path.join(cfg["bm25_index_path"], "bm25_model.pkl")
    try:
        with open(bm25_file_path, "rb") as f:
            bm25_data = pickle.load(f)
            bm25 = bm25_data["bm25"]
            all_nodes = bm25_data["nodes"]
    except Exception as e:
        raise RuntimeError(f"Error loading BM25 index: {e}") from e

    reranker = None
    if cfg["reranker_enabled"]:
        print(f"Loading reranker {cfg['reranker_model']}...")
        reranker = CrossEncoder(cfg["reranker_model"], max_length=512)

    return cfg, semantic_retriever, bm25, all_nodes, reranker


def run_hybrid_query(user_input, cfg, semantic_retriever, bm25, all_nodes, reranker):
    """Run one hybrid query; return answer and per-stage retrieval details for UIs."""
    semantic_results = semantic_retriever.retrieve(user_input)
    semantic_nodes_scores = [(n.node, n.score) for n in semantic_results]

    query_tokens = user_input.lower().split()
    bm25_scores = bm25.get_scores(query_tokens)
    bm25_results = sorted(enumerate(bm25_scores), key=lambda x: x[1], reverse=True)[
        : cfg["bm25_top_k"]
    ]
    bm25_nodes_scores = [(all_nodes[idx], score) for idx, score in bm25_results]

    fused = rrf_fusion(semantic_nodes_scores, bm25_nodes_scores)
    top_fused = fused[: cfg["fusion_top_k"]]

    if reranker is not None:
        pairs = [(user_input, n.get_content()) for n, _ in top_fused]
        reranker_scores = reranker.predict(pairs)
        reranked = sorted(
            zip([n for n, _ in top_fused], reranker_scores), key=lambda x: x[1], reverse=True
        )
        final_results = reranked[: cfg["reranker_top_k"]]
    else:
        final_results = top_fused[: cfg["reranker_top_k"]]

    context_str = "\n\n".join([n.get_content() for n, _ in final_results])
    prompt = f"Question: {user_input}\nContext:\n{context_str}\nAnswer:"
    response = Settings.llm.complete(prompt)
    answer = str(response).strip()

    def pack_nodes(nodes_scores, score_key="score"):
        rows = []
        for node, score in nodes_scores:
            rows.append(
                {
                    "filename": node.metadata.get("file_name", "Unknown"),
                    score_key: float(score),
                    "snippet": _node_snippet(node),
                }
            )
        return rows

    semantic_rows = pack_nodes(semantic_nodes_scores)
    bm25_rows = pack_nodes(bm25_nodes_scores)
    fused_rows = [
        {
            "filename": n.metadata.get("file_name", "Unknown"),
            "rrf_score": float(s),
            "snippet": _node_snippet(n),
        }
        for n, s in top_fused
    ]
    final_rows = []
    for node, score in final_results:
        final_rows.append(
            {
                "filename": node.metadata.get("file_name", "Unknown"),
                "score": float(score),
                "snippet": _node_snippet(node),
            }
        )

    return {
        "answer": answer,
        "prompt": prompt,
        "semantic": semantic_rows,
        "bm25": bm25_rows,
        "fused": fused_rows,
        "final": final_rows,
    }


def main():
    print("Loading 02_Advanced_RAG Query Engine...")
    import config

    try:
        cfg, semantic_retriever, bm25, all_nodes, reranker = load_advanced_pipeline(config)
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print("\n" + "=" * 50)
    print("🤖 Advanced Hybrid RAG Ready!")
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
            out = run_hybrid_query(user_input, cfg, semantic_retriever, bm25, all_nodes, reranker)

            print("\n" + "=" * 10 + " ANSWER " + "=" * 10)
            print(out["answer"])

            print("\n" + "=" * 10 + " SOURCES " + "=" * 9)
            for idx, row in enumerate(out["final"], 1):
                snip = row["snippet"].replace("\n", " ")
                short = snip[:80] + "..." if len(snip) > 80 else snip
                print(f"[{idx}] {row['filename']} (Score: {row['score']:.4f}) -> {short}")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
