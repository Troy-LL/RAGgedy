# 02 Advanced RAG Answer Key

Use this as the expected reference flow for the advanced hybrid pipeline.

## Correct sequence

1. Ingest and index documents for dense retrieval.
2. Build BM25 sparse index.
3. Run query through dense retriever and BM25 retriever.
4. Fuse both result sets with RRF.
5. Rerank fused candidates with cross-encoder.
6. Build grounded prompt from reranked context.
7. Generate final answer.

## Correct command combinations

```bash
python ingest.py
python query.py --question "How does reranking improve quality?" --visualize popup
```

One-command runner equivalent:

```bash
python run.py --path advanced --dataset edu_scholar --question "How does reranking improve quality?" --visualize popup
```

## Correct visualization interpretation

- `Question -> Dense+BM25`: query fans out to two retrieval strategies.
- `Dense+BM25 -> RRF Fusion`: rank lists are combined.
- `RRF Fusion -> Rerank`: cross-encoder prioritizes best evidence.
- `Rerank -> Response`: final grounded answer is generated.

## Healthy output characteristics

- Dense and BM25 stages both produce candidates.
- Fused pool contains mixed evidence candidates.
- Final reranked sources are coherent and relevant.
- Final answer aligns with reranked sources.
