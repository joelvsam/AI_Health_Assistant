from fastapi import FastAPI
from backend.routes.medicines import router as medicine_router
from backend.routes.documents import router as document_router
from backend.routes.ai_explain import router as ai_router
from backend.database import init_db

app = FastAPI(title="AI Health Assistant")

# Initialize database on startup
@app.on_event("startup")
def startup():
    init_db()

# Include routers
app.include_router(medicine_router)
app.include_router(document_router)
app.include_router(ai_router)

@app.get("/")
def root():
    return {"status": "running"}
