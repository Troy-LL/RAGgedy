from ..core.orchestrator import Orchestrator
from ..llm.local_clients import OllamaClient
from ..retrieval.in_memory import InMemoryRetriever


def build_local_orchestrator(model: str, base_url: str) -> Orchestrator:
    return Orchestrator(
        mode="local",
        retriever=InMemoryRetriever(),
        llm=OllamaClient(model=model, base_url=base_url),
    )
