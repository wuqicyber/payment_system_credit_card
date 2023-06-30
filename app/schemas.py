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

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models import TransactionType

class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    balance: float
    credit_limit: float
    transactions: List["Transaction"]

    class Config:
        orm_mode = True


class TransactionBase(BaseModel):
    amount: float
    transaction_category: TransactionType
    due_date: Optional[datetime] = None
    repayment_status: bool = False


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: int
    user_id: int
    timestamp: datetime
    interest_and_penalty: "InterestAndPenalty"

    class Config:
        orm_mode = True


class InterestAndPenaltyBase(BaseModel):
    interest_rate: float = 0.003
    interest_amount: float
    penalty_rate: float = 0.003
    penalty_amount: float


class InterestAndPenaltyCreate(InterestAndPenaltyBase):
    pass


class InterestAndPenalty(InterestAndPenaltyBase):
    id: int
    transaction_id: int

    class Config:
        orm_mode = True


