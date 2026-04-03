import time

from .interfaces import LLMClient, Retriever
from .types import AnswerBundle


class Orchestrator:
    def __init__(self, mode: str, retriever: Retriever, llm: LLMClient):
        self.mode = mode
        self.retriever = retriever
        self.llm = llm

    def ask(self, question: str, top_k: int = 3, include_trace: bool = False) -> AnswerBundle:
        t0 = time.perf_counter()
        chunks = self.retriever.retrieve(question, top_k)

        context = "\n\n".join(
            [f"[{c.source}] {c.text}" for c in chunks]
        )
        prompt = (
            "You are a grounded assistant. Answer using only the context below.\n"
            f"Question: {question}\n"
            f"Context:\n{context}\n"
            "Final answer:"
        )
        answer = self.llm.generate(prompt)
        elapsed_ms = round((time.perf_counter() - t0) * 1000.0, 2)

        trace: list[str] = []
        if include_trace:
            trace.append("Thought (simulated): I should retrieve the most relevant chunks first.")
            trace.append(f"Action: Retrieved top {len(chunks)} chunks by lexical overlap.")
            trace.append("Result: Built a grounded prompt and generated a final answer.")

        return AnswerBundle(
            mode=self.mode,
            question=question,
            answer=answer.strip(),
            chunks=chunks,
            trace=trace,
            metadata={"latency_ms": elapsed_ms, "top_k": top_k},
        )
