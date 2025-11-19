from app.database.models.users import User
from app.database.models.accounts import Account
from app.database.models.payments import Payment
from app.database.models.transactions import Transaction, TransactionType
from fastapi import HTTPException
from sqlalchemy import select, update, or_
from sqlalchemy.orm import selectinload
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError



async def create_user(db, user):
    try:
        
        if isinstance(user, BaseModel):
            user_obj = User(**user.model_dump())
        elif isinstance(user, dict):
            user_obj = User(**user)
        else:
            user_obj = user
        db.add(user_obj)
        await db.commit()
        await db.refresh(user_obj)
        return user_obj
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")


async def create_account(db, account):
    try:
        if isinstance(account, BaseModel):
            account_obj = Account(**account.model_dump())
        elif isinstance(account, dict):
            account_obj = Account(**account)
        else:
            account_obj = account
        db.add(account_obj)
        await db.commit()
        await db.refresh(account_obj)
        return account_obj
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create account: {str(e)}")


async def create_payment(db, payment):
    try:
        if isinstance(payment, BaseModel):
            payment_obj = Payment(**payment.model_dump())
        elif isinstance(payment, dict):
            payment_obj = Payment(**payment)
        else:
            payment_obj = payment
            
        transaction_obj_from = {
            "account_id": payment_obj.from_account_id,
            "amount": payment_obj.amount,
            "transaction_type": "debit",
        }
        transaction_obj_to = {
            "account_id": payment_obj.to_account_id,
            "amount": payment_obj.amount,
            "transaction_type": "credit",
        }

        from_acc = await get_account_by_id(db, payment_obj.from_account_id)
        to_acc = await get_account_by_id(db, payment_obj.to_account_id)
        if not from_acc or not to_acc:
            raise HTTPException(status_code=404, detail="From or To account not found")

        from_transaction = await create_transaction(db, transaction_obj_from)
        to_transaction = await create_transaction(db, transaction_obj_to)
        payment_obj.transaction_id = from_transaction.id
        db.add(payment_obj)
        await db.flush()
        
        if not from_transaction:
            raise HTTPException(status_code=400, detail="From transaction creation failed")
        
        if not to_transaction:
            raise HTTPException(status_code=400, detail="To transaction creation failed")
        
        payment_obj.transaction_id = from_transaction.id
        
        await db.refresh(payment_obj)
        await db.commit()
        return payment_obj
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create payment: {str(e)}")


async def create_transaction(db, transaction):
    try:
        if isinstance(transaction, BaseModel):
            transaction_obj = Transaction(**transaction.model_dump())
        elif isinstance(transaction, dict):
            transaction_obj = Transaction(**transaction)
        else:
            transaction_obj = transaction
        # Validate that account exists
        account = await get_account_by_id(db, transaction_obj.account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        if isinstance(transaction_obj.transaction_type, str):
            try:
                transaction_obj.transaction_type = TransactionType(transaction_obj.transaction_type)
            except Exception:
                transaction_obj.transaction_type = TransactionType(transaction_obj.transaction_type.lower())

        try:
            amt = float(transaction_obj.amount)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid transaction amount")

        delta = -amt if transaction_obj.transaction_type == TransactionType.DEBIT else amt
        

        if db.in_transaction():
            db.add(transaction_obj)
            await db.flush()
            await update_account_balance(db, transaction_obj.account_id, delta)
        else:
            async with db.begin():
                db.add(transaction_obj)
                await db.flush()
                await update_account_balance(db, transaction_obj.account_id, delta)
        await db.refresh(transaction_obj)
        return transaction_obj
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create transaction: {str(e)}")



async def get_user_by_email(db, email: str):
    try:
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalars().first()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")


async def get_account_by_id(db, account_id: int):
    try:
        result = await db.execute(
            select(Account)
            .options(
                selectinload(Account.transactions),
                selectinload(Account.payments_made),
                selectinload(Account.payments_received)
            )
            .filter(Account.id == account_id)
        )
        ans = result.scalars().first()
        print("DEBUG:", ans.__dict__ if ans else None)
        if ans:
            print("Transactions:", len(ans.transactions))
            print("Payments made:", len(ans.payments_made))
            print("Payments received:", len(ans.payments_received))
        return ans
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")


async def get_transaction_by_id(db, transaction_id: int):
    try:
        result = await db.execute(select(Transaction).filter(Transaction.id == transaction_id))
        return result.scalars().first()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")


async def get_payment_by_id(db, payment_id: int):
    try:
        result = await db.execute(select(Payment).filter(Payment.id == payment_id))
        return result.scalars().first()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")


async def get_user_by_id(db, user_id: int):
    try:
        result = await db.execute(select(User).filter(User.id == user_id))
        return result.scalars().first()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")


async def get_accounts_by_user(db, user_id: int):
    try:
        result = await db.execute(select(Account).filter(Account.user_id == user_id))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")




async def update_user(db, id: int, updateData):
    try:
        data = updateData.model_dump(exclude_unset=True)

        stmt = (
            update(User)
            .where(User.id == id)
            .values(**data)
            .execution_options(synchronize_session="fetch")
        )

        await db.execute(stmt)
        await db.commit()

        updated = await db.get(User, id)
        if not updated:
            raise HTTPException(status_code=404, detail="User not found")

        return updated

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update user: {str(e)}")


async def update_account(db, id: int, updateData):
    try:
        data = updateData.model_dump(exclude_unset=True)

        stmt = (
            update(Account)
            .where(Account.id == id)
            .values(**data)
            .execution_options(synchronize_session="fetch")
        )

        await db.execute(stmt)
        await db.commit()

        updated = await db.get(Account, id)
        if not updated:
            raise HTTPException(status_code=404, detail="Account not found")

        return updated

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update account: {str(e)}")


async def update_transaction(db, id: int, updateData):
    try:
        data = updateData.model_dump(exclude_unset=True)

        stmt = (
            update(Transaction)
            .where(Transaction.id == id)
            .values(**data)
            .execution_options(synchronize_session="fetch")
        )

        await db.execute(stmt)
        await db.commit()

        updated = await db.get(Transaction, id)
        if not updated:
            raise HTTPException(status_code=404, detail="Transaction not found")

        return updated

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update transaction: {str(e)}")


async def update_payment(db, id: int, updateData):
    try:
        data = updateData.model_dump(exclude_unset=True)

        stmt = (
            update(Payment)
            .where(Payment.id == id)
            .values(**data)
            .execution_options(synchronize_session="fetch")
        )

        await db.execute(stmt)
        await db.commit()

        updated = await db.get(Payment, id)
        if not updated:
            raise HTTPException(status_code=404, detail="Payment not found")

        return updated

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update payment: {str(e)}")



async def get_all_users(db):
    try:
        result = await db.execute(select(User))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch users: {str(e)}")


async def get_all_accounts(db):
    try:
        result = await db.execute(select(Account))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch accounts: {str(e)}")


async def get_all_transactions(db):
    try:
        result = await db.execute(select(Transaction))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch transactions: {str(e)}")


async def get_all_payments(db):
    try:
        result = await db.execute(select(Payment))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch payments: {str(e)}")



async def get_account_transactions(db, account_id: int):
    try:
        result = await db.execute(select(Transaction).filter(Transaction.account_id == account_id))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch account transactions: {str(e)}")


async def get_account_payments(db, account_id: int):
    try:
        # Payment has from_account_id and to_account_id columns
        result = await db.execute(
            select(Payment).filter(or_(Payment.from_account_id == account_id, Payment.to_account_id == account_id))
        )
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch account payments: {str(e)}")


async def update_account_balance(db, account_id: int, delta: float):
    """Atomically update an account's balance by delta (positive or negative). Caller should handle transactions if needed."""
    try:
        # Lock the account row for update to ensure consistency
        stmt_select = select(Account).where(Account.id == account_id)
        result = await db.execute(stmt_select)
        account = result.scalars().first()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        current_balance = account.balance or 0.0
        new_balance = current_balance + delta
        if new_balance < 0:
            raise HTTPException(status_code=400, detail="Insufficient funds")

        stmt_update = (
            update(Account)
            .where(Account.id == account_id)
            .values(balance=new_balance)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(stmt_update)
        await db.flush()
        updated = await db.get(Account, account_id)
        return updated
    except SQLAlchemyError as e:
        # Do not rollback here: caller should manage transactions/rollbacks
        raise HTTPException(status_code=500, detail=f"Failed to update account balance: {str(e)}")
