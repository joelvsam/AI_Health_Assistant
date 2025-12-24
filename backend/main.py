from fastapi import FastAPI
from backend.routes.medicines import router as medicine_router
from backend.database import init_db

app = FastAPI(title="AI Health Assistant")

# Initialize database on startup
@app.on_event("startup")
def startup():
    init_db()

# Include medicine routes
app.include_router(medicine_router)

@app.get("/")
def root():
    return {"status": "running"}
