# Zero-Barrier Runtime

Runnable three-tier runtime scaffold:
- Tier 1: Mock mode (simulated learning trace)
- Tier 2: API mode (Groq/Together/Hugging Face)
- Tier 3: Local mode (Ollama)

Reference expected flow and outputs: [ANSWER_KEY.md](ANSWER_KEY.md)

You can also run all project paths from one command at repo root:

```bash
python run.py --path mock --show-trace
python run.py --path demo
python run.py --path naive --dataset edu_scholar
python run.py --path advanced --dataset edu_scholar
```

## Run

From repository root:

```bash
python -m zero_barrier_runtime.app --mode mock --question "Why does retrieval matter?" --show-trace
```

By default, the runtime uses native popup visualization (no localhost). Use `--visualize terminal` for console-only output.

### API mode

```bash
set MODEL_PROVIDER=groq
set MODEL_NAME=llama-3.1-8b-instant
set MODEL_API_KEY=your_key
python -m zero_barrier_runtime.app --mode api --question "Explain embeddings for beginners"
```

### Local mode

```bash
ollama pull llama3.1:8b
python -m zero_barrier_runtime.app --mode local --local-model llama3.1:8b --question "How does reranking help?"
```

## Polished Tier 1 Demo

```bash
python -m zero_barrier_runtime.scripts.mock_trace_demo
```

Visualization flags supported by runtime and demo:

- `--visualize auto` popup with terminal fallback (default)
- `--visualize popup` force popup
- `--visualize terminal` print only
- `--visualize off` no rendering output
