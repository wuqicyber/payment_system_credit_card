from fastapi import FastAPI
from app.controllers import user_controller, transaction_controller
import uvicorn
app = FastAPI()

# Include routers
app.include_router(user_controller.router, prefix="/api", tags=["users"])
app.include_router(transaction_controller.router, prefix="/api", tags=["transactions"])
# app.include_router(repayment_controller.router, prefix="/api", tags=["repayments"])
# app.include_router(account_controller.router, prefix="/api", tags=["accounts"])

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True, access_log=True)



# 是的，但是余额balance也需要相应地进行变化，另外，只有当transaction_category为payment与withdrawl时，due_date与
# repayment_status才需要有值，transaction_category为repayment时，这两个字段的值为None。
# repayment相应要对每个payement和withdrawl进行还款。还款后，payment与withdrwal的repayment_status更新为1
# 还款金额等于本金加利息加罚息。余额balance的记法由你自己决定。