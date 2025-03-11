from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Account(BaseModel):
    name: str
    AccNo: str
    mobileNo: str  # Fixed typo from "mobileNO" to "mobileNo"
    balance: int

class DepositRequest(BaseModel):
    amount: int  # Amount to deposit

class WithdrawRequest(BaseModel):
    amount : int


data = {
    0: Account(name="manish", AccNo="1001", mobileNo="8306612960", balance=1000),
    1: Account(name="roshan", AccNo="1002", mobileNo="8306612961", balance=1000),
    2: Account(name="karmveer", AccNo="1003", mobileNo="8306612962", balance=1000),
    3: Account(name="priyanshu", AccNo="1004", mobileNo="8306612963", balance=1000),
    4: Account(name="abhishek", AccNo="1005", mobileNo="8306612964", balance=1000),
}


@app.get("/data/")
async def totalAcc():
    return data

@app.get("/account/{AccNo}")
async def AccInformation(AccNo:str):
    for account in data.values():
        if account.AccNo == AccNo:
            return account

    raise HTTPException(status_code=404, detail="Account not found")

@app.put("/account/{AccNo}/deposit")
async def add_money(AccNo:str, deposit:DepositRequest):
    for account in data.values():
        if account.AccNo == AccNo:
            if deposit.amount <= 0:
                raise HTTPException(status_code = 404,  detail = "amount must be greater than 0")
            
            account.balance = account.balance + deposit.amount
            return {"message": f"{deposit.amount} deposit successfully!", "New balance": account.balance}

            raise HTTPException(status_code=404, detail="Account not found")

@app.put("/account/{AccNo}/withdraw")
async def withdraw(AccNo:str, withdraw: WithdrawRequest):
    for account in data.values():
        if account.AccNo == AccNo:
            if withdraw.amount <= 0:
                raise HTTPException(status_code = 404,  detail = "amount must be greater than 0")

            account.balance = account.balance - withdraw.amount
            return {"message": f"{withdraw.amount} withdraw successfully!", "New balance": account.balance}

            raise HTTPException(status_code=404, detail="Account not found")

@app.post("/account/")
async def add_account(account: Account):
    # Check if account number already exists
    for acc in data.values():
        if acc.AccNo == account.AccNo:
            raise HTTPException(status_code=400, detail="Account number already exists")

    # Add account to dictionary
    new_id = max(data.keys()) + 1  # Generate a new ID
    data[new_id] = account
    return {"message": "Account added successfully", "account": account}

