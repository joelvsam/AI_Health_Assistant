from fastapi import APIRouter
from backend.core.security import hash_password, create_token
from backend.database import get_connection

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(email: str, password: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (email, password, is_admin) VALUES (?, ?, 0)",
        (email, hash_password(password))
    )
    conn.commit()
    conn.close()
    return {"token": create_token({"email": email})}
