from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext

from backend.database import get_connection
from backend.core.security import create_token

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# --------- Schemas ---------

class AuthRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# --------- Helpers ---------

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


# --------- Routes ---------

@router.post("/register", response_model=AuthResponse)
def register(payload: AuthRequest):
    conn = get_connection()
    cur = conn.cursor()

    # Check if user exists
    cur.execute("SELECT id FROM users WHERE email = ?", (payload.email,))
    if cur.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="User already exists")

    cur.execute(
        "INSERT INTO users (email, password, is_admin) VALUES (?, ?, 0)",
        (payload.email, hash_password(payload.password))
    )

    conn.commit()
    conn.close()

    token = create_token({"email": payload.email, "role": "user"})
    return {"access_token": token}


@router.post("/login", response_model=AuthResponse)
def login(payload: AuthRequest):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT password, is_admin FROM users WHERE email = ?",
        (payload.email,)
    )
    row = cur.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    hashed_password, is_admin = row

    if not verify_password(payload.password, hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    role = "admin" if is_admin else "user"
    token = create_token({"email": payload.email, "role": role})

    return {"access_token": token}
