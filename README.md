# AI-Powered Personal Health and Medical Planner

A project focused on building a HealthTech solution that helps users manage medicines, understand medical documents, and access reliable health education in one place.

> Note: This system provides non-diagnostic guidance only and does not replace professional medical advice.

## Project Overview

The AI-Powered Personal Health and Medical Planner is designed to support individuals in organizing their healthcare routines and understanding medical information using generative AI. The platform combines reminders, AI-based explanations, and trusted educational content to promote healthier daily habits.

## Core Features

- Medicine manager for tracking dosage, timing, and frequency
- AI chat for basic health-related questions (non-diagnostic)
- Medical document explainer for reports and test results
- Health education hub with trusted resources

## Requirements

- Python 3.10+ for local setup
- Optional: Docker and Docker Compose
- Optional: Hugging Face API token for AI features

## Installation (Local)

1. Create and activate a virtual environment.

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

For macOS or Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Configure environment variables.

Create a `.env` file in the project root:

```env
JWT_SECRET=change-me
HUGGINGFACEHUB_API_TOKEN=your-token-here
```

4. Run the backend.

```bash
uvicorn backend.main:app --reload
```

5. Open the app in your browser:

```
http://localhost:8000
```

## Installation (Docker)

```bash
docker compose up --build
```

Then open:

```
http://localhost:8000
```

## Notes

- The SQLite database is stored at `backend/healthhub.db`.
- To reset data, stop the app and delete `backend/healthhub.db`.
