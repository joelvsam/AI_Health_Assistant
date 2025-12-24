from fastapi import FastAPI
from backend.routes.medicines import router as medicine_router
from backend.routes.documents import router as document_router
from backend.database import init_db

app = FastAPI(title="AI Health Assistant")

# Initialize database on startup
@app.on_event("startup")
def startup():
    init_db()

# Include routes
app.include_router(medicine_router)
app.include_router(document_router)

@app.get("/")
def root():
    return {"status": "running"}
