from fastapi import APIRouter

# Create a new router for reminder endpoints
router = APIRouter(prefix="/reminders", tags=["Reminders"])

@router.get("/")
def reminder_info():
    """
    Get reminder information.
    """
    return {"status": "handled by backend scheduler"}