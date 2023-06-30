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

from app.services.transaction_service import TransactionService
from app.models import Transaction, InterestAndPenalty
from app.services.user_service import UserService
from app.models import TransactionType
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models import User

router = APIRouter()

@router.post("/transactions/{user_id}/payment")
def payment(user_id: int, amount: float, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    transaction_service = TransactionService(db)
    transaction = transaction_service.create_transaction(user_id, amount, TransactionType.payment)
    if transaction is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Payment successful"}

@router.post("/transactions/{user_id}/repayment")
def repayment(user_id: int, amount: float, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    transaction_service = TransactionService(db)
    user_service = UserService(db)

    # 找到所有未偿还的付款和提款，并按时间戳排序
    unpaid_transactions = db.query(Transaction).filter(Transaction.user_id == user_id, Transaction.repayment_status == False).order_by(Transaction.timestamp).all()

    for transaction in unpaid_transactions:
        total_amount = transaction.remained_unpaid_amount + transaction_service.calculate_interest_and_penalty(transaction)

        # 如果还款金额足够偿还这笔交易
        if amount >= total_amount:
            amount -= total_amount
            transaction.repayment_status = True
            transaction.remained_unpaid_amount = 0
            user_service.update_balance(user_id, -total_amount)  # 更新用户余额
            db.commit()
        else:
            transaction.remained_unpaid_amount -= amount
            amount = 0
            db.commit()
            break

    if amount > 0:
        # 如果还有剩余的还款金额，将其添加到用户的余额中
        user_service.update_balance(user_id, amount)

    return {"message": "Repayment successful"}


@router.post("/transactions/{user_id}/withdrawal")
def withdrawal(user_id: int, amount: float, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    transaction_service = TransactionService(db)
    transaction = transaction_service.create_transaction(user_id, amount, TransactionType.withdrawal)
    if transaction is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Withdrawal successful"}

@router.get("/transactions/{user_id}/get_transactions")
def get_transactions(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    transaction_service = TransactionService(db)
    transactions = transaction_service.get_transactions(user_id)
    if transactions is None:
        raise HTTPException(status_code=404, detail="User not found")
    return transactions

# 你需要考虑的是这个利息的计算，余额应该算上利息与罚息，罚息是过了还款时间之后根据未还款金额增加的利息。每次还款按照时间戳抵消每一笔消费与提现。
