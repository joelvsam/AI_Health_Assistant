from fastapi import FastAPI
from backend.routes.medicines import router as medicine_router
from backend.database import init_db
from backend.reminder import start_scheduler
import threading

app = FastAPI(title="AI Health Assistant")

# Initialize database and start reminder scheduler on startup
@app.on_event("startup")
def startup():
    init_db()
    threading.Thread(target=start_scheduler, daemon=True).start()

# Include medicine routes
app.include_router(medicine_router)

# Simple root endpoint
@app.get("/")
def root():
    return {"status": "running"}
