import re

from ..core.types import RetrievedChunk


DEFAULT_CORPUS = [
    {
        "id": "doc-1",
        "source": "librarian_basics.txt",
        "text": "Chunking splits long documents into smaller pieces so retrieval can find precise facts.",
    },
    {
        "id": "doc-2",
        "source": "embedding_map_pins.txt",
        "text": "Embeddings convert text into vectors, placing similar meanings near each other.",
    },
    {
        "id": "doc-3",
        "source": "grounding_notes.txt",
        "text": "Retrieval helps reduce hallucinations by giving the model trusted context before answering.",
    },
    {
        "id": "doc-4",
        "source": "reranking_notes.txt",
        "text": "Reranking reorders candidate chunks so the most relevant context appears first.",
    },
    {
        "id": "doc-5",
        "source": "agentic_loop.txt",
        "text": "Agentic loops can plan, retrieve again, verify, and then produce a better final response.",
    },
]


def _tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


class InMemoryRetriever:
    def __init__(self, corpus: list[dict] | None = None):
        self.corpus = corpus or DEFAULT_CORPUS

    def retrieve(self, query: str, top_k: int) -> list[RetrievedChunk]:
        q = _tokenize(query)
        scored: list[RetrievedChunk] = []
        for row in self.corpus:
            t = _tokenize(row["text"])
            overlap = len(q & t)
            score = overlap / max(len(q), 1)
            scored.append(
                RetrievedChunk(
                    chunk_id=row["id"],
                    source=row["source"],
                    text=row["text"],
                    score=score,
                )
            )

        scored.sort(key=lambda c: c.score, reverse=True)
        return scored[: max(1, top_k)]
