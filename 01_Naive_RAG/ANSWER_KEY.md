# 01 Naive RAG Answer Key

Use this as the expected reference flow for this module.

## Correct sequence

1. Ingest documents into chunks and embeddings.
2. Store embeddings in vector DB.
3. Convert question into retrieval query.
4. Retrieve top-k passages from vector DB.
5. Build prompt plus retrieved context.
6. Generate final answer from grounded context.

## Correct command combinations

```bash
python ingest.py
python query.py --question "Why does chunking help?" --visualize popup
```

One-command runner equivalent:

```bash
python run.py --path naive --dataset edu_scholar --question "Why does chunking help?" --visualize popup
```

## Correct visualization interpretation

- `Question -> Embed Search`: user query is prepared for dense retrieval.
- `Embed Search -> Retrieve`: vector DB returns top-k chunks.
- `Retrieve -> Generate`: retrieved chunks become prompt context.
- `Generate -> Response`: model returns grounded answer.

## Healthy output characteristics

- At least one retrieved source is shown.
- Source snippets relate directly to the question.
- Answer reflects retrieved content rather than generic text.
- Latency is reported.
