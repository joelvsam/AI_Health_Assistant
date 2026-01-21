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

app = FastAPI(title="AI Health Assistant")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize database on startup
@app.on_event("startup")
def startup():
    init_db()
    # Start the reminder scheduler in a background thread
    scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()

# Include routers
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(medicine_router)
app.include_router(reminders_router)
app.include_router(ai_router)
app.include_router(documents_router)
app.include_router(chat_router)
app.include_router(notifications_router)

@app.get("/")
def root():
    return {"status": "running"}
