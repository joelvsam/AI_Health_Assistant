FROM python:3.10-slim

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app
ENV PYTHONPATH=/app

# System dependencies for OCR, PDFs, and ML packages
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    poppler-utils \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy all application code
COPY . .

# Store the SQLite DB under backend/data so the compose volume persists it.
# .dockerignore excludes *.db, so remove any stale file before linking.
RUN mkdir -p /app/backend/data \
    && rm -f /app/backend/healthhub.db \
    && ln -s /app/backend/data/healthhub.db /app/backend/healthhub.db

# Expose FastAPI port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
