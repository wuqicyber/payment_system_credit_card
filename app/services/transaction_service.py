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

from app.models import Transaction, User, TransactionType, InterestAndPenalty
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

class TransactionService:
    def __init__(self, db: Session):
        self.db = db

    def create_transaction(self, user_id: int, amount: float, transaction_type: TransactionType):
        user = self.db.query(User).filter(User.id == user_id).first()
        if user is None:
            return None

        due_date = None
        repayment_status = None
        remained_unpaid_amount = None
        if transaction_type in [TransactionType.payment, TransactionType.withdrawal]:
            due_date = datetime.now() + timedelta(days=30)
            repayment_status = False
            remained_unpaid_amount = amount

        transaction = Transaction(user_id=user_id, amount=amount, transaction_category=transaction_type, due_date=due_date, repayment_status=repayment_status, remained_unpaid_amount=remained_unpaid_amount)
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)

        interest_and_penalty = InterestAndPenalty(transaction_id=transaction.id, interest_rate=0.003, interest_amount=amount*0.003, penalty_rate=0.003, penalty_amount=0)
        self.db.add(interest_and_penalty)
        self.db.commit()
        self.db.refresh(interest_and_penalty)

        # 更新用户余额
        if transaction_type == TransactionType.payment:
            user.balance -= amount
        elif transaction_type == TransactionType.withdrawal:
            user.balance -= amount
        elif transaction_type == TransactionType.repayment:
            user.balance += amount
        self.db.commit()

        return transaction

    # ... 其他函数 ...


    def get_transactions(self, user_id: int):
        transactions = self.db.query(Transaction).filter(Transaction.user_id == user_id).all()
        return transactions

    def calculate_interest_and_penalty(self, transaction: Transaction):
        interest_and_penalty = self.db.query(InterestAndPenalty).filter(
                InterestAndPenalty.transaction_id == transaction.id).first()
        if transaction.repayment_status or transaction.transaction_category == TransactionType.repayment:
            return 0
        days = (datetime.now() - transaction.timestamp).days
        due_days = (transaction.due_date - transaction.timestamp).days
        if days <= due_days:
            return transaction.remained_unpaid_amount * interest_and_penalty.interest_rate * days
        else:
            return transaction.remained_unpaid_amount * (
                        interest_and_penalty.interest_rate * due_days + interest_and_penalty.penalty_rate * (
                            days - due_days))

