import sqlite3
from backend.database import get_connection
from backend.models.user import UserCreate, UserOut
from backend.core.security import hash_password

def create_user(user: UserCreate):
    conn = get_connection()
    cur = conn.cursor()
    hashed_pass = hash_password(user.password)
    cur.execute(
        "INSERT INTO users (email, password, is_admin) VALUES (?, ?, 0)",
        (user.email, hashed_pass)
    )
    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    return user_id

def get_user_by_email(email: str) -> UserOut | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, email, is_admin FROM users WHERE email = ?",
        (email,)
    )
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return UserOut(id=row[0], email=row[1], is_admin=row[2])

def get_user_for_auth(email: str) -> dict | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, email, password, is_admin FROM users WHERE email = ?",
        (email,)
    )
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return {
        "id": row[0],
        "email": row[1],
        "password": row[2],
        "is_admin": row[3]
    }
