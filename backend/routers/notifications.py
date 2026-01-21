from fastapi import APIRouter, Depends
from backend.database import get_connection
from backend.routers.auth import get_current_user
from backend.models.user import UserOut

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/")
def get_notifications(current_user: UserOut = Depends(get_current_user)):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, message, created_at FROM notifications WHERE user_id = ? AND is_read = 0 ORDER BY created_at DESC", (current_user.id,))
    notifications = cur.fetchall()
    conn.close()
    return [dict(row) for row in notifications]

@router.post("/{notification_id}/read")
def mark_as_read(notification_id: int, current_user: UserOut = Depends(get_current_user)):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE notifications SET is_read = 1 WHERE id = ? AND user_id = ?", (notification_id, current_user.id))
    conn.commit()
    conn.close()
    return {"message": "Notification marked as read"}
