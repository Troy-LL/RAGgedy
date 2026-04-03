from ..core.orchestrator import Orchestrator
from ..llm.cloud_clients import CloudLLMClient
from ..retrieval.in_memory import InMemoryRetriever


def build_api_orchestrator(provider: str, model: str, api_key: str) -> Orchestrator:
    return Orchestrator(
        mode="api",
        retriever=InMemoryRetriever(),
        llm=CloudLLMClient(provider=provider, model=model, api_key=api_key),
    )
