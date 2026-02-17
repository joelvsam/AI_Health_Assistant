# backend/main.py
"""
This is the main entry point for the AI Health Assistant application.
It initializes the FastAPI app, includes the API routers, and serves the frontend.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import threading
from backend.routers.medicines import router as medicine_router
from backend.routers.reminders import router as reminders_router
from backend.routers.admin import router as admin_router
from backend.routers.auth import router as auth_router
from backend.routers.ai_explain import router as ai_router
from backend.routers.documents import router as documents_router
from backend.routers.chat import router as chat_router
from backend.routers.notifications import router as notifications_router
from backend.database import init_db
from backend.core.config import FRONTEND_DIR, FRONTEND_STATIC_DIR, LANDING_PAGE
from backend.reminder import start_scheduler
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Create a FastAPI app instance
app = FastAPI(title="AI Health Assistant")

# Add CORS middleware to allow cross-origin requests from any origin.
# This is useful for development, but should be restricted in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize the database on application startup
@app.on_event("startup")
def startup():
    """
    Initializes the database and starts the reminder scheduler in a background thread.
    This function is called once when the application starts.
    """
    init_db()
    # Start the reminder scheduler in a background thread
    scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()

# Include the API routers for different functionalities of the application.
# Each router handles a specific set of endpoints.
app.include_router(auth_router, prefix="/api", tags=["Authentication"])
app.include_router(admin_router, prefix="/api", tags=["Admin"])
app.include_router(medicine_router, prefix="/api", tags=["Medicines"])
app.include_router(reminders_router, prefix="/api", tags=["Reminders"])
app.include_router(ai_router, prefix="/api", tags=["AI"])
app.include_router(documents_router, prefix="/api", tags=["Documents"])
app.include_router(chat_router, prefix="/api", tags=["Chat"])
app.include_router(notifications_router, prefix="/api", tags=["Notifications"])

# Serve the frontend static files (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory=str(FRONTEND_STATIC_DIR)), name="static")

# Serve the landing page at the root URL
@app.get("/")
async def read_index():
    """
    Returns the landing page of the frontend.
    This is the first page the user will see.
    """
    return FileResponse(str(LANDING_PAGE))

# Serve other frontend pages
@app.get("/{catchall:path}")
async def serve_frontend_pages(catchall: str):
    """
    Serves other frontend HTML pages based on the path.
    If the file is not found, it returns a 404 error.
    """
    file_path = FRONTEND_DIR / catchall
    if file_path.exists() and file_path.is_file():
        return FileResponse(str(file_path))
    # This is a fallback for any route that is not found
    return {"status": "Not Found"}
