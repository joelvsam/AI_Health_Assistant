from fastapi import APIRouter

router = APIRouter(prefix="/reminders", tags=["Reminders"])

@router.get("/")
def reminder_info():
    return {"status": "handled by backend scheduler"}
