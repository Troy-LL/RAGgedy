# Live pipeline visualization

A small [Streamlit](https://streamlit.io/) app that runs **ingestion** with a **live log** and **queries** with a **step-by-step** view of retrieval and generation.

## Setup

Install the dependencies for the module you use (**01** or **02**), then install Streamlit:

```bash
pip install -r ../01_Naive_RAG/requirements.txt
pip install -r requirements.txt
```

For Advanced RAG, use `02_Advanced_RAG/requirements.txt` instead of (or in addition to) module 01.

## Run (standalone)

From the **repository root** (so paths resolve correctly):

```bash
streamlit run visualization/app.py
```

Or from this folder:

```bash
cd visualization
streamlit run app.py
```

Set **Dataset scenario** in the sidebar (same as `RAGGEDY_DATASET`, default `edu_scholar`). Run **Ingest** first for that module and dataset, then use the **Query** tab.

## Run (integrated from modules)

To avoid separate visualization setup, launch from each module directly:

```bash
python 01_Naive_RAG/visualize.py --dataset edu_scholar
python 02_Advanced_RAG/visualize.py --dataset edu_scholar
```

When launched this way:

- Module and dataset are preconfigured automatically.
- Sidebar controls for module and dataset are locked (no manual tinkering).
- Optional auto-ingest on startup:

```bash
python 01_Naive_RAG/visualize.py --dataset edu_scholar --auto-ingest
```

## What you see

- **Ingest**: subprocess runs `python -u ingest.py` with unbuffered output so the log updates as the pipeline runs.
- **Query**: loads the same engines as `query.py` and shows dense retrieval, then (module 02) BM25, RRF fusion, rerank, and the final answer.
