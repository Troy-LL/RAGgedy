"""
Streamlit UI: live ingest logs + step-by-step query visualization for RAGgedy modules.
Run from repo root: streamlit run visualization/app.py
"""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import streamlit as st

REPO_ROOT = Path(__file__).resolve().parent.parent
SUPPORTED_MODULES = {"01_Naive_RAG", "02_Advanced_RAG"}


def _env_flag(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _load_module_from_path(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {file_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@st.cache_resource
def _naive_bundle(dataset_id: str):
    os.environ["RAGGEDY_DATASET"] = dataset_id
    cfg = _load_module_from_path(
        f"naive_cfg_{dataset_id}", REPO_ROOT / "01_Naive_RAG" / "config.py"
    )
    qm = _load_module_from_path(
        f"naive_query_{dataset_id}", REPO_ROOT / "01_Naive_RAG" / "query.py"
    )
    engine = qm.load_naive_query_engine(cfg)
    return engine, qm.run_naive_query


@st.cache_resource
def _advanced_bundle(dataset_id: str):
    os.environ["RAGGEDY_DATASET"] = dataset_id
    cfg_mod = _load_module_from_path(
        f"adv_cfg_{dataset_id}", REPO_ROOT / "02_Advanced_RAG" / "config.py"
    )
    qm = _load_module_from_path(
        f"adv_query_{dataset_id}", REPO_ROOT / "02_Advanced_RAG" / "query.py"
    )
    cfg, sem_ret, bm25, nodes, reranker = qm.load_advanced_pipeline(cfg_mod)
    return cfg, sem_ret, bm25, nodes, reranker, qm.run_hybrid_query


def _run_ingest(module_subdir: str, dataset_id: str, log_placeholder) -> int:
    module_dir = REPO_ROOT / module_subdir
    env = os.environ.copy()
    env["RAGGEDY_DATASET"] = dataset_id
    env["PYTHONUNBUFFERED"] = "1"
    proc = subprocess.Popen(
        [sys.executable, "-u", "ingest.py"],
        cwd=str(module_dir),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    lines: list[str] = []
    assert proc.stdout is not None
    for line in proc.stdout:
        lines.append(line)
        log_placeholder.code("".join(lines), language="text")
    proc.wait()
    return proc.returncode


def main():
    st.set_page_config(
        page_title="RAGgedy — live pipeline",
        page_icon="🧩",
        layout="wide",
    )
    st.title("RAGgedy — live pipeline")
    st.caption(
        "Stream ingestion logs in real time and inspect each retrieval stage on query."
    )

    preset_module = os.getenv("RAGGEDY_VIS_MODULE", "").strip()
    preset_dataset = (os.getenv("RAGGEDY_DATASET", "") or "").strip()
    auto_ingest = _env_flag("RAGGEDY_VIS_AUTO_INGEST", default=False)
    if preset_module and preset_module not in SUPPORTED_MODULES:
        st.error(
            f"Invalid RAGGEDY_VIS_MODULE '{preset_module}'. "
            "Use one of: 01_Naive_RAG, 02_Advanced_RAG."
        )
        return

    settings_locked = bool(preset_module)
    default_module = preset_module or "01_Naive_RAG"
    default_dataset = preset_dataset or "edu_scholar"

    with st.sidebar:
        st.header("Settings")
        module_options = ["01_Naive_RAG", "02_Advanced_RAG"]
        module_idx = module_options.index(default_module)
        module = st.radio(
            "Module",
            module_options,
            index=module_idx,
            disabled=settings_locked,
            help="Module is preconfigured by launcher" if settings_locked else None,
        )
        dataset_id = st.text_input(
            "Dataset scenario (`RAGGEDY_DATASET`)",
            value=default_dataset,
            disabled=settings_locked,
            help="Dataset is preconfigured by launcher" if settings_locked else None,
        )
        if st.button("Clear cached models"):
            st.cache_resource.clear()
            st.success("Cache cleared. Reload the page or run again after re-ingesting.")

    ingest_tab, query_tab = st.tabs(["Ingest (live log)", "Query (live stages)"])

    with ingest_tab:
        ds = dataset_id.strip() or "edu_scholar"
        st.markdown(
            f"Runs `{module}/ingest.py` with **`RAGGEDY_DATASET={ds}`** and streams stdout here."
        )
        log_box = st.empty()
        run_ingest_clicked = st.button("Run ingestion", type="primary", key="ingest_btn")
        should_auto_run = auto_ingest and not st.session_state.get("_raggedy_auto_ingest_done")
        if should_auto_run:
            st.session_state["_raggedy_auto_ingest_done"] = True

        if run_ingest_clicked or should_auto_run:
            log_box.code("", language="text")
            status_label = "Ingestion auto-started..." if should_auto_run else "Ingestion running..."
            with st.status(status_label, expanded=True) as status:
                code = _run_ingest(module, ds, log_box)
                if code == 0:
                    status.update(label="Ingestion finished", state="complete")
                else:
                    status.update(label=f"Ingestion exited with code {code}", state="error")

    with query_tab:
        ds = dataset_id.strip() or "edu_scholar"
        st.markdown("Load the same engines as `query.py` and walk through each stage.")

        if module == "01_Naive_RAG":
            try:
                qe, run_naive = _naive_bundle(ds)
            except RuntimeError as e:
                st.error(str(e))
                return
            except Exception as e:
                st.exception(e)
                return

            user_q = st.chat_input("Ask a question (naive RAG)…", key="naive_chat")
            if user_q:
                with st.chat_message("user"):
                    st.write(user_q)
                with st.chat_message("assistant"):
                    with st.spinner("Retrieving and generating…"):
                        structured = run_naive(qe, user_q)
                    st.markdown("**Answer**")
                    st.write(structured["answer"])
                    with st.expander("Retrieved sources (dense)", expanded=True):
                        for i, s in enumerate(structured["sources"], 1):
                            st.markdown(
                                f"**{i}.** `{s['filename']}` · score `{s['score']}`"
                            )
                            st.caption(s["snippet"])

        else:
            try:
                cfg, sem_ret, bm25, nodes, reranker, run_hybrid = _advanced_bundle(ds)
            except RuntimeError as e:
                st.error(str(e))
                return
            except Exception as e:
                st.exception(e)
                return

            user_q = st.chat_input("Ask a question (hybrid RAG)…", key="adv_chat")
            if user_q:
                with st.chat_message("user"):
                    st.write(user_q)
                with st.chat_message("assistant"):
                    prog = st.progress(0.0)
                    out = run_hybrid(user_q, cfg, sem_ret, bm25, nodes, reranker)
                    prog.progress(1.0)

                    st.markdown("**Answer**")
                    st.write(out["answer"])

                    c1, c2 = st.columns(2)
                    with c1:
                        with st.expander("1 · Dense (semantic)", expanded=True):
                            st.dataframe(
                                out["semantic"], use_container_width=True, hide_index=True
                            )
                    with c2:
                        with st.expander("2 · BM25 (sparse)", expanded=True):
                            st.dataframe(
                                out["bm25"], use_container_width=True, hide_index=True
                            )
                    with st.expander("3 · RRF fusion pool", expanded=False):
                        st.dataframe(
                            out["fused"], use_container_width=True, hide_index=True
                        )
                    with st.expander("4 · After cross-encoder rerank", expanded=True):
                        st.dataframe(
                            out["final"], use_container_width=True, hide_index=True
                        )


if __name__ == "__main__":
    main()
