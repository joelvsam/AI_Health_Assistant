from fastapi import FastAPI, HTTPException
from typing import List
from database import SessionLocal, engine, Base
import models, schemas, crud

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Health Assistant Backend",
    description="Backend API for Health Education Hub and AI Summarization",
    version="0.1"
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------------------
# Article Endpoints (CRUD)
# ----------------------------

@app.get("/articles", response_model=List[schemas.Article])
def read_articles(skip: int = 0, limit: int = 10, db=next(get_db())):
    return crud.get_articles(db, skip=skip, limit=limit)

@app.post("/articles", response_model=schemas.Article)
def create_article(article: schemas.ArticleCreate, db=next(get_db())):
    return crud.create_article(db=db, article=article)

# ----------------------------
# Video Endpoints (CRUD)
# ----------------------------

@app.get("/videos", response_model=List[schemas.Video])
def read_videos(skip: int = 0, limit: int = 10, db=next(get_db())):
    return crud.get_videos(db, skip=skip, limit=limit)

@app.post("/videos", response_model=schemas.Video)
def create_video(video: schemas.VideoCreate, db=next(get_db())):
    return crud.create_video(db=db, video=video)

# ----------------------------
# AI Placeholder Endpoints
# ----------------------------

@app.post("/video-summary")
def summarize_video(video_text: dict):
    # Placeholder: replace with AI summarization later
    return {"summary": "This is a placeholder summary. Replace with AI logic."}

@app.post("/query")
def ai_query(query: dict):
    # Placeholder: replace with AI chatbot logic later
    return {"answer": "This is a placeholder AI response. Replace with AI logic."}

