# Tutorial Module (ELI5): RAG Like a Storybook

## Who This Is For

If words like "embedding" and "retriever" feel scary, this is for you.

## Big Idea

RAG is like writing homework with a helpful librarian:

- You ask a question.
- Librarian finds the best books.
- You write using only those books, not random guesses.

---

## 1) Embeddings = Magic Map Pins 📍

ELI5 metaphor:
- Imagine every sentence gets a tiny map pin.
- Similar ideas are pinned near each other.
- Different ideas are far away.

Why it matters:
- The system can find related meaning, not just exact matching words.

How to play:
- Ask two similar questions and compare retrieved chunks.
- Change chunk size and see which pins become "closer".

---

## 2) Retrieval = The Librarian 📚

ELI5 metaphor:
- Instead of reading the whole library, your librarian grabs the top 3 books.

Why it matters:
- Faster answers and less nonsense.

How to play:
- Try `top_k=2` vs `top_k=8`.
- Notice when too little context misses facts and too much context adds noise.

---

## 3) Reranking = The Neat Stack 🧱

ELI5 metaphor:
- You found 10 books. Reranking puts the best 3 on top.

Why it matters:
- Better context at the top means better final answers.

How to play:
- Turn reranking on and off.
- Compare confidence and relevance.

---

## 4) Agentic Loop = The Careful Detective 🕵️

ELI5 metaphor:
- Detective checks clues, notices gaps, asks for one more clue, then answers.

Why it matters:
- Multi-step checking can reduce mistakes.

How to play:
- Enable loop mode for hard questions.
- Track each step: plan, retrieve, verify, answer.

---

## 5) Three Tiers = Three Playground Levels 🎮

### Tier 1: Theoretical Sandbox (Mock)

Metaphor:
- Toy kitchen where kids learn cooking steps safely.

Why it matters:
- You learn the flow instantly without spending money.

How to play:
- Run mock mode and inspect the staged trace:
- Thought: "What should I look up?"
- Action: "Search chunks 1..k"
- Result: "Best grounded answer"

### Tier 2: Cloud Pilot (API)

Metaphor:
- Food delivery app: real chef cooks, you just order.

Why it matters:
- Real model quality, no heavyweight setup.

How to play:
- Try the same question on Llama and Mistral.
- Compare speed, style, and factual grounding.

### Tier 3: Local Titan (On-Prem)

Metaphor:
- Cooking in your own kitchen with your own tools.

Why it matters:
- Privacy, control, and offline usage.

How to play:
- Run local model, then unplug internet and test again.
- Benchmark latency and quality against API mode.

---

## Mini Missions (Hands-On)

1. Ask: "Why do we split documents into chunks?"
2. Run in all three tiers.
3. Write one sentence on what changed in answer quality and speed.

---

## Friendly Truth

RAG is not about making models smarter.
RAG is about giving models the right notebook before the test.
