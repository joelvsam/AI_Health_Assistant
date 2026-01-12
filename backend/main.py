from fastapi import FastAPI
from backend.routers.medicines import router as medicine_router
from backend.routers.reminders import router as reminders_router
from backend.routers.admin import router as admin_router
from backend.routers.auth import router as auth_router
from backend.routers.ai_explain import router as ai_router
from backend.database import init_db

app = FastAPI(title="AI Health Assistant")

# Initialize database on startup
@app.on_event("startup")
def startup():
    init_db()

# Include routers
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(medicine_router)
app.include_router(reminders_router)
app.include_router(ai_router)

@app.get("/")
def root():
    return {"status": "running"}
