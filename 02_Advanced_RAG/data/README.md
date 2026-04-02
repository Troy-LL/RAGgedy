# Edu-Scholar Dataset 👩‍🏫

The **Edu-Scholar** dataset is a purpose-built, synthetic student-tutor dataset for CET (College Entrance Test) preparation. 

It is designed to be small enough to run fully locally in under 5 minutes while still providing meaningful results for RAG evaluations.

---

## 📊 Dataset Structure

| Subject | Passages | Length (Avg tokens) |
|---|---|---|
| **Biology** | ~20 | 150-400 |
| **Physics** | ~15 | 150-400 |
| **Mathematics** | ~15 | 150-400 |
| **English** | ~10 | 150-400 |

### `passages/`
Contains raw `.txt` files parsed by `ingest.py`. 

### `questions.json`
Contains 50+ Q&A pairs used by `evaluation/eval_naive.py` to calculate Ragas scores. Each entry includes:
- `question`: The student query.
- `answer`: The ground-truth answer.
- `source_passage`: The filename where the answer exists.

---

## 🧪 Evaluation Baseline

The "Good" pipeline configuration targets:
- **Faithfulness**: ≥ 0.55
- **Context Precision**: ≥ 0.60

The "Broken" pipeline results in significantly lower scores, demonstrating the importance of chunking and retrieval granularity.
