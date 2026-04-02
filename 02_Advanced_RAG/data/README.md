# Data directory

Passages and evaluation questions live under **`datasets/<scenario_id>/`**.

- **Default scenario**: `edu_scholar` (CET-style synthetic passages).
- **Switch scenario**: set environment variable `RAGGEDY_DATASET` to the folder name under `datasets/` before running `ingest.py`, `query.py`, or evaluation scripts.

```powershell
# Windows PowerShell
$env:RAGGEDY_DATASET = "edu_scholar"
python ingest.py
```

Each scenario folder should contain:

- `passages/` — `.txt` files for retrieval
- `questions.json` — optional Q&A pairs for evaluation

Semantic and BM25 indexes are stored per scenario under `.chroma/<scenario_id>/` and `.bm25_index/<scenario_id>/`.

See [datasets/README.md](datasets/README.md) for how to add a new scenario.
