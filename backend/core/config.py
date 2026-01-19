import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = BASE_DIR / "healthhub.db"
FAISS_PATH = BASE_DIR / "data" / "faiss_index"

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-later")
JWT_ALGORITHM = "HS256"
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
