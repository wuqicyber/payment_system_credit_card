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

from sqlalchemy import Column, Integer, Float, ForeignKey, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func
from enum import Enum
from sqlalchemy import Enum as SQLEnum

class TransactionType(Enum):
    withdrawal = "withdrawal"
    payment = "payment"
    repayment = "repayment"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(200), nullable=False)
    balance = Column(Float, default=0)  # replaced from Account table
    credit_limit = Column(Float, default=1000.0)
    transactions = relationship("Transaction", back_populates="user")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)  # this is the purchase amount
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    transaction_category = Column(SQLEnum(TransactionType))  # using TransactionType Enum
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    due_date = Column(DateTime(timezone=True))  # the date by which the purchase should be repaid
    repayment_status = Column(Boolean, default=False)  # false if not repaid, true if repaid
    remained_unpaid_amount = Column(Float)

    user = relationship("User", back_populates="transactions")
    interest_and_penalty = relationship("InterestAndPenalty", uselist=False, back_populates="transaction")

class InterestAndPenalty(Base):
    __tablename__ = "interests_and_penalties"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=False)
    interest_rate = Column(Float, nullable=False, default=0.003)
    interest_amount = Column(Float, nullable=False)
    penalty_rate = Column(Float, nullable=False, default=0.003)  # set an appropriate penalty rate
    penalty_amount = Column(Float, nullable=False)

    transaction = relationship("Transaction", back_populates="interest_and_penalty")
# 我修改了transaction的表结构，增加了一个remained_unpaid_amount在逾期时计算罚息时按照这个未还款金额来计算，按天计算罚息
