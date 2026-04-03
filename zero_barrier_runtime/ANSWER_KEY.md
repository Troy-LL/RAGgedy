# Zero Barrier Runtime Answer Key

Use this as the expected reference behavior for runtime paths.

## Path meanings

- `mock`: simulated end-to-end flow for teaching and debugging.
- `api`: cloud model provider path.
- `local`: Ollama/local model path.
- `demo`: polished mock walkthrough script.

## Correct sequence (runtime)

1. Parse question and runtime settings.
2. Retrieve top-k chunks.
3. Build grounded context.
4. Generate answer via selected mode.
5. Return answer plus metadata and optional trace.

## Correct command combinations

```bash
python run.py --path mock --show-trace --visualize popup
python run.py --path demo --visualize popup
python run.py --path api --question "Explain vector embeddings like I am 5" --visualize popup
python run.py --path local --question "How does retrieval improve answer quality?" --visualize popup
```

## Correct visualization interpretation

- Animated dot indicates active transition.
- `Current Step` explains what is happening now.
- `Stage Guide` explains each node role.
- `Characteristics` reports run metadata (top-k, retrieved count, latency).

## Healthy output characteristics

- Question, retrieved context, and final answer are present.
- Trace appears when `--show-trace` is enabled.
- Metadata includes latency and top-k.
