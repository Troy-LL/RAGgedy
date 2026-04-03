# Visualization Module Answer Key

Use this as the expected reference for the standalone Streamlit visualization.

## Correct sequence

1. Select module and dataset (or use module-bound launcher).
2. Run ingestion for selected module/dataset.
3. Run query in the Query tab.
4. Inspect stage outputs and final answer.

## Correct command combinations

Standalone Streamlit:

```bash
streamlit run visualization/app.py
```

Module-bound launchers:

```bash
python 01_Naive_RAG/visualize.py --dataset edu_scholar
python 02_Advanced_RAG/visualize.py --dataset edu_scholar
```

## Correct visualization interpretation

Naive module:

- Retrieved source list should map to answer content.

Advanced module:

- Semantic table, BM25 table, fused pool, and reranked final table should appear in order.

## Healthy output characteristics

- Ingestion log updates live without buffering stalls.
- Query output includes answer and evidence.
- Dataset/module pairing is consistent between ingest and query.
