from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr

from backend.core.security import create_token, verify_password, decode_token
from backend.models.user import UserCreate, UserOut
from backend.crud.user import create_user, get_user_by_email, get_user_for_auth


router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# --------- Schemas ---------

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    email: str
    password: str


# --------- Dependencies ---------

def get_current_user(token: str = Depends(oauth2_scheme)) -> UserOut:
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_user_by_email(payload["email"])
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


# --------- Routes ---------

@router.post("/register", response_model=AuthResponse)
def register(payload: UserCreate):
    # Check if user exists
    if get_user_by_email(payload.email):
        raise HTTPException(status_code=400, detail="User already exists")

    user = create_user(payload)

    token = create_token({"sub": str(user.id), "name": user.name, "email": user.email, "role": "user"})
    return {"access_token": token}


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest):
    user = get_user_for_auth(payload.email)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(payload.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    role = "admin" if user["is_admin"] else "user"
    token = create_token({"sub": str(user["id"]), "name": user["name"], "email": user["email"], "role": role})
    return {"access_token": token}


@router.get("/users/me", response_model=UserOut)
def read_users_me(current_user: UserOut = Depends(get_current_user)):
    return current_user
