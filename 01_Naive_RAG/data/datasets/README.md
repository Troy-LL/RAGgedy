# Dataset scenarios

Each **scenario** is a self-contained folder: one corpus (`passages/`) plus optional `questions.json` for evaluation.

| Folder | Description |
|--------|-------------|
| **edu_scholar** | Default synthetic student–tutor dataset for CET-style prep (see that folder’s README). |

## Adding a scenario

1. Create `datasets/<your_id>/passages/` and add `.txt` files.
2. Optionally add `datasets/<your_id>/questions.json` with entries: `question`, `answer`, `source_passage` (match evaluation scripts in this repo).
3. Run with `RAGGEDY_DATASET=<your_id>` so ingest and query use the new paths and a separate Chroma store under `.chroma/<your_id>/`.

Use a short, filesystem-safe id (letters, numbers, underscores).
