from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = BASE_DIR / "healthhub.db"
FAISS_PATH = BASE_DIR / "data" / "faiss_index"

JWT_SECRET = "dev-secret-change-later"
JWT_ALGORITHM = "HS256"
