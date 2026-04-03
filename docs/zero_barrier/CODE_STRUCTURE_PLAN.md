# Code Structure Plan: Zero-Barrier Three-Tier Model

## Goal

Separate the product into clear mode adapters so the same user flow works across:
- Mock mode (simulated)
- API mode (hosted open-source models)
- Local mode (on-device models)

## Design Principles

- One orchestrator, many runtimes.
- Shared interfaces so tiers can be swapped with a single flag.
- No mode-specific logic in UI/CLI.
- Deterministic mock traces for education and testing.

## Suggested Layout

```text
src/
  core/
    interfaces.py      # Abstract contracts for Retriever and LLMClient
    types.py           # Request, RetrievedChunk, ReasoningTrace, AnswerBundle
    orchestrator.py    # Shared pipeline: retrieve -> reason -> respond
  modes/
    mock_mode.py       # Hard-coded retrieval + chain-of-thought-like visible trace
    api_mode.py        # Provider adapters for Groq/Together/Hugging Face
    local_mode.py      # Adapters for Ollama/vLLM/llama.cpp
  retrieval/
    in_memory.py       # For mock mode and small demos
    chroma_adapter.py  # Optional vector store adapter
    bm25_adapter.py    # Optional sparse retrieval
    hybrid.py          # Optional fusion strategy
  llm/
    groq_client.py
    together_client.py
    huggingface_client.py
    ollama_client.py
  config/
    settings.py        # Env parsing and validation
    mode_registry.py   # Maps mode name -> concrete runtime wiring
  ui/
    cli.py             # Single entrypoint for all tiers
```

## Runtime Contract

```python
class Retriever:
    def retrieve(self, query: str, top_k: int) -> list[RetrievedChunk]:
        ...

class LLMClient:
    def generate(self, prompt: str) -> str:
        ...
```

## Orchestrator Behavior

1. Parse user question.
2. Retrieve context chunks.
3. Build prompt with citations.
4. Call model adapter.
5. Return answer bundle:
- final answer
- used context
- optional reasoning trace
- latency + mode metadata

## Tier Mapping

### Tier 1: Theoretical Sandbox

- Retriever: `in_memory.py` with fixed chunks.
- LLM: `mock_mode.py` with scripted response patterns.
- Output: Includes educational trace with stages:
- Thought (simulated)
- Action (retrieve/rank/respond)
- Result (final answer)

### Tier 2: Cloud Pilot

- Retriever: `chroma_adapter.py` or in-memory starter.
- LLM: `groq_client.py`, `together_client.py`, `huggingface_client.py`.
- Provider selected via env:
- `MODEL_PROVIDER`
- `MODEL_NAME`
- `MODEL_API_KEY`

### Tier 3: Local Titan

- Retriever: same as API mode.
- LLM: `ollama_client.py` or other local runtime adapter.
- Local config:
- `LOCAL_MODEL_NAME`
- `LOCAL_BASE_URL`

## Configuration Matrix

| Setting | Mock | API | Local |
|---|---:|---:|---:|
| `APP_MODE` | required | required | required |
| `MODEL_PROVIDER` | no | yes | no |
| `MODEL_API_KEY` | no | yes | no |
| `LOCAL_MODEL_NAME` | no | no | yes |
| `TOP_K` | optional | optional | optional |

## Testing Strategy

- Unit tests on `orchestrator.py` with fake adapters.
- Snapshot tests for mock traces.
- Smoke tests for each mode path.
- Contract tests ensuring all adapters respect `LLMClient` interface.

## DX Outcomes

- Beginners can run mode 1 in minutes.
- Practitioners can evaluate mode 2 with no GPU.
- Power users can move to mode 3 without rewriting app logic.
