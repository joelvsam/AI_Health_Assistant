from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

from backend.core.security import create_token, verify_password
from backend.models.user import UserCreate
from backend.crud.user import create_user, get_user_by_email, get_user_for_auth


router = APIRouter(prefix="/auth", tags=["Auth"])


# --------- Schemas ---------

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# --------- Routes ---------

@router.post("/register", response_model=AuthResponse)
def register(payload: UserCreate):
    # Check if user exists
    if get_user_by_email(payload.email):
        raise HTTPException(status_code=400, detail="User already exists")

    create_user(payload)

    token = create_token({"email": payload.email, "role": "user"})
    return {"access_token": token}


@router.post("/login", response_model=AuthResponse)
def login(payload: UserCreate):
    user = get_user_for_auth(payload.email)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(payload.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    role = "admin" if user["is_admin"] else "user"
    token = create_token({"email": user["email"], "role": role})

    return {"access_token": token}
