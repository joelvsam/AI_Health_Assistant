import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
REPO_DIR = BASE_DIR.parent

def _resolve_path(value: str | None, default: Path, base: Path) -> Path:
    if not value:
        return default
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = base / path
    return path

DATABASE_PATH = _resolve_path(
    os.getenv("DATABASE_PATH"),
    BASE_DIR / "healthhub.db",
    REPO_DIR,
)
FAISS_PATH = _resolve_path(
    os.getenv("FAISS_PATH"),
    BASE_DIR / "data" / "faiss_index",
    REPO_DIR,
)

FRONTEND_DIR = _resolve_path(
    os.getenv("FRONTEND_DIR"),
    REPO_DIR / "frontend",
    REPO_DIR,
)
FRONTEND_STATIC_DIR = _resolve_path(
    os.getenv("FRONTEND_STATIC_DIR"),
    FRONTEND_DIR / "static",
    REPO_DIR,
)
LANDING_PAGE = _resolve_path(
    os.getenv("LANDING_PAGE"),
    FRONTEND_DIR / "landing.html",
    REPO_DIR,
)

TESSERACT_CMD = os.getenv("TESSERACT_CMD")

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-later")
JWT_ALGORITHM = "HS256"
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
