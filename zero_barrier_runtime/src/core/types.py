from dataclasses import dataclass, field
from typing import Any


@dataclass
class RetrievedChunk:
    chunk_id: str
    source: str
    text: str
    score: float


@dataclass
class AnswerBundle:
    mode: str
    question: str
    answer: str
    chunks: list[RetrievedChunk] = field(default_factory=list)
    trace: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
