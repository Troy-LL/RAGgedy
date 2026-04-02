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

import config

def rrf_fusion(semantic_nodes_with_scores, bm25_nodes_with_scores, k=60):
    # semantic_nodes_with_scores is list of (node, score)
    # bm25_nodes_with_scores is list of (node, score)
    
    # rank them
    fusion_scores = {}
    node_mapping = {}
    
    # Process semantic
    for rank, (node, _) in enumerate(semantic_nodes_with_scores):
        if node.node_id not in fusion_scores:
            fusion_scores[node.node_id] = 0
            node_mapping[node.node_id] = node
        fusion_scores[node.node_id] += 1 / (rank + k)
        
    # Process BM25
    for rank, (node, _) in enumerate(bm25_nodes_with_scores):
        if node.node_id not in fusion_scores:
            fusion_scores[node.node_id] = 0
            node_mapping[node.node_id] = node
        fusion_scores[node.node_id] += 1 / (rank + k)
        
    # Sort
    fused = sorted(fusion_scores.items(), key=lambda x: x[1], reverse=True)
    return [(node_mapping[nid], score) for nid, score in fused]

def main():
    print("Loading 02_Advanced_RAG Query Engine...")
    cfg = config.CONFIG

    # Configure Global Settings
    Settings.llm = Ollama(model=cfg["llm_model"], base_url=cfg["ollama_host"], request_timeout=60.0)
    Settings.embed_model = HuggingFaceEmbedding(model_name=cfg["embedding_model"])
    
    # Load ChromaDB
    try:
        db = chromadb.PersistentClient(path=cfg["chroma_db_path"])
        chroma_collection = db.get_collection("advanced_rag_collection")
    except Exception as e:
        print(f"Error: Could not load ChromaDB index from {cfg['chroma_db_path']}. {e}")
        sys.exit(1)

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)
    semantic_retriever = VectorIndexRetriever(index=index, similarity_top_k=cfg["semantic_top_k"])
    
    # Load BM25
    bm25_file_path = os.path.join(cfg["bm25_index_path"], "bm25_model.pkl")
    try:
        with open(bm25_file_path, "rb") as f:
            bm25_data = pickle.load(f)
            bm25 = bm25_data["bm25"]
            all_nodes = bm25_data["nodes"]
    except Exception as e:
        print(f"Error loading BM25 index: {e}")
        sys.exit(1)
        
    # Load Reranker
    if cfg["reranker_enabled"]:
        print(f"Loading reranker {cfg['reranker_model']}...")
        reranker = CrossEncoder(cfg["reranker_model"], max_length=512)
    else:
        reranker = None

    print("\n" + "="*50)
    print("🤖 Advanced Hybrid RAG Ready!")
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
            
            # Step 1: Semantic Retrieval
            semantic_results = semantic_retriever.retrieve(user_input)
            semantic_nodes_scores = [(n.node, n.score) for n in semantic_results]
            
            # Step 2: BM25 Retrieval
            query_tokens = user_input.lower().split()
            bm25_scores = bm25.get_scores(query_tokens)
            bm25_results = sorted(enumerate(bm25_scores), key=lambda x: x[1], reverse=True)[:cfg["bm25_top_k"]]
            bm25_nodes_scores = [(all_nodes[idx], score) for idx, score in bm25_results]
            
            # Step 3: Fusion
            fused = rrf_fusion(semantic_nodes_scores, bm25_nodes_scores)
            top_fused = fused[:cfg["fusion_top_k"]]
            
            # Step 4: Reranking
            if reranker is not None:
                pairs = [(user_input, n.get_content()) for n, _ in top_fused]
                reranker_scores = reranker.predict(pairs)
                
                reranked = sorted(zip([n for n, _ in top_fused], reranker_scores), key=lambda x: x[1], reverse=True)
                final_results = reranked[:cfg["reranker_top_k"]]
            else:
                final_results = top_fused[:cfg["reranker_top_k"]]
                
            # Step 5: Answer Generation
            context_str = "\n\n".join([n.get_content() for n, _ in final_results])
            prompt = f"Question: {user_input}\nContext:\n{context_str}\nAnswer:"
            
            response = Settings.llm.complete(prompt)
            
            print("\n" + "="*10 + " ANSWER " + "="*10)
            print(str(response).strip())
            
            print("\n" + "="*10 + " SOURCES " + "="*9)
            for idx, (node, score) in enumerate(final_results, 1):
                content = node.get_content().replace('\n', ' ')
                snippet = content[:80] + "..." if len(content) > 80 else content
                filename = node.metadata.get('file_name', 'Unknown')
                print(f"[{idx}] {filename} (Score: {score:.4f}) -> {snippet}")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
