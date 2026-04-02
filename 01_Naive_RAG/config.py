import os

# Base directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Active dataset: folder name under data/datasets/<id>/
DATASET_ID = (os.environ.get("RAGGEDY_DATASET", "edu_scholar") or "edu_scholar").strip()
DATASET_DIR = os.path.join(DATA_DIR, "datasets", DATASET_ID)
PASSAGES_DIR = os.path.join(DATASET_DIR, "passages")
QUESTIONS_FILE = os.path.join(DATASET_DIR, "questions.json")
CHROMA_DIR = os.path.join(BASE_DIR, ".chroma", DATASET_ID)

# Vector DB Settings
COLLECTION_NAME = f"{DATASET_ID}_naive"

# Models
# Embedding model used to convert text to high-dimensional vectors
EMBED_MODEL = "BAAI/bge-m3"
# Local LLM model utilized for answering queries
LLM_MODEL = "llama3"
# Local LLM endpoint URL (assumes Ollama is running)
LLM_BASE_URL = "http://localhost:11434"

# Retrieval Settings
CHUNK_SIZE = 512
CHUNK_OVERLAP = 64
TOP_K = 5

# Evaluation Targets
RAGAS_FAITHFULNESS_TARGET = 0.55
RAGAS_CONTEXT_PRECISION_TARGET = 0.60
