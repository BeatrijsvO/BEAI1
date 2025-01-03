import os
from pathlib import Path

PORT = os.getenv("PORT", "8000")
FAISS_DIR = Path("./faiss_store")