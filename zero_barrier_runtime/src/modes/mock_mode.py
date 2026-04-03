from ..core.orchestrator import Orchestrator
from ..retrieval.in_memory import InMemoryRetriever


class MockReasonerClient:
    def generate(self, prompt: str) -> str:
        return (
            "Simulated answer: Chunking helps retrieval fetch precise context, "
            "which improves grounded responses and lowers hallucination risk."
        )


def build_mock_orchestrator() -> Orchestrator:
    return Orchestrator(
        mode="mock",
        retriever=InMemoryRetriever(),
        llm=MockReasonerClient(),
    )
