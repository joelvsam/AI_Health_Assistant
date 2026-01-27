# backend/main.py

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
from backend.reminder import start_scheduler
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Create a FastAPI app instance
app = FastAPI(title="AI Health Assistant")

# Add CORS middleware to allow cross-origin requests
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
    """Initializes the database and starts the reminder scheduler."""
    init_db()
    # Start the reminder scheduler in a background thread
    scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()

# Include the API routers for different functionalities
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(medicine_router)
app.include_router(reminders_router)
app.include_router(ai_router)
app.include_router(documents_router)
app.include_router(chat_router)
app.include_router(notifications_router)

# Serve the frontend static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Serve the landing page at the root URL
@app.get("/")
async def read_index():
    """Returns the landing page of the frontend."""
    return FileResponse('frontend/landing.html')

# Serve other frontend pages
@app.get("/{catchall:path}")
async def serve_frontend_pages(catchall: str):
    """Serves other frontend HTML pages."""
    file_path = os.path.join("frontend", catchall)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    # This is a fallback for any route that is not found
    return {"status": "Not Found"}