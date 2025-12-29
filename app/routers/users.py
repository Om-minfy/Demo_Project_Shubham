from fastapi import APIRouter, HTTPException
from app.schemas import User, UserCreate
from app.storage import users, user_id_counter
from app.auth import create_access_token

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=User)
def register_user(user: UserCreate):
    global user_id_counter

    for u in users:
        if u["email"] == user.email:
            raise HTTPException(status_code=400, detail="Email already exists")

    new_user = {
        "id": user_id_counter,
        "name": user.name,
        "email": user.email,
        "password": user.password
    }

    users.append(new_user)
    user_id_counter += 1
    return new_user

@router.post("/login")
def login_user(user: UserCreate):
    for u in users:
        if u["email"] == user.email and u["password"] == user.password:
            token = create_access_token(u["id"])
            return {"access_token": token, "user_id": u["id"]}
    raise HTTPException(status_code=400, detail="Invalid credentials")