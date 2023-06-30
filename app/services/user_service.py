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


from app.schemas import UserCreate
from app.models import User
from app.core.security import get_password_hash
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.core.security import verify_password
from app import models, schemas


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate):
        hashed_password = get_password_hash(user.password)
        db_user = User(username=user.username, hashed_password=hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def authenticate_user(self, db: Session, username: str, password: str):
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user

    def get_balance_and_credit_limit(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()
        if user is None:
            return None
        return user.balance, user.credit_limit

    def update_password(self, user_id: int, new_password: str):
        user = self.db.query(User).filter(User.id == user_id).first()
        if user is None:
            return None
        hashed_password = get_password_hash(new_password)
        user.hashed_password = hashed_password
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_balance(self, user_id: int, amount: float):
        user = self.db.query(User).filter(User.id == user_id).first()
        if user is None:
            return None
        user.balance += amount
        self.db.commit()
        self.db.refresh(user)
        return user


