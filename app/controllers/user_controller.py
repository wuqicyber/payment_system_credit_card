"""

   ┏┓   ┏┓ + +
  ┏┛┻━━━┛┻┓ + +
  ┃   ━   ┃ ++ + + +
  ┃ ████━████  ┃+
  ┃       ┃ +
  ┃   ┻   ┃ + +
  ┗━┓   ┏━┛
    ┃   ┃ + + + +
    ┃   ┃ +   神兽保佑,代码无bug
    ┃   ┃ +
    ┃   ┗━━━┓ + +
    ┃       ┣┓
    ┃       ┏┛
    ┗┓┓┏━┳┓┏┛ + + + +
     ┃┫┫ ┃┫┫
     ┗┻┛ ┗┻┛+ + + +

Create Time: 2023/6/30

"""

from app.services.user_service import UserService
from app.schemas import UserCreate
from app.models import User
from sqlalchemy import exists
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db, get_redis
from datetime import timedelta
from app.auth import create_access_token, get_current_user
import redis

router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/users/register")
def register(user: UserCreate, db: Session = Depends(get_db), redis_db: redis.Redis = Depends(get_redis)):
    username_exists = db.query(exists().where(User.username == user.username)).scalar()
    if username_exists:
        raise HTTPException(status_code=400, detail="Username already exists")

    user_service = UserService(db)

    # 创建用户
    db_user = user_service.create_user(user)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User already registered")

    return {
        "username": db_user.username,
        "user_id": db_user.id,
        "password": db_user.hashed_password,
        "balance": db_user.balance,
        "credit_limit": db_user.credit_limit
    }


@router.post("/users/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = UserService(db).authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}  # Return the token as a JSON response


@router.get("/users/{user_id}/balance_and_credit_limit")
def get_balance_and_credit_limit(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"balance": user.balance, "credit_limit": user.credit_limit}

@router.put("/users/{user_id}/password")
def update_password(user_id: int, new_password: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    updated_user = UserService(db).update_password(user_id, new_password)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Password updated successfully"}


