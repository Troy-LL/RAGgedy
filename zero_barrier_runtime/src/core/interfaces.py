from typing import Protocol

from .types import RetrievedChunk


class Retriever(Protocol):
    def retrieve(self, query: str, top_k: int) -> list[RetrievedChunk]:
        ...


class LLMClient(Protocol):
    def generate(self, prompt: str) -> str:
        ...
