from sqlalchemy.orm import Session
from sqlalchemy import func
import models, schemas
from auth import get_password_hash
from datetime import datetime

# User CRUD
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Transaction CRUD
def get_transactions(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Transaction).filter(
        models.Transaction.user_id == user_id
    ).offset(skip).limit(limit).all()

def create_transaction(db: Session, transaction: schemas.TransactionCreate, user_id: int):
    db_transaction = models.Transaction(**transaction.dict(), user_id=user_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def update_transaction(db: Session, transaction_id: int, transaction: schemas.TransactionUpdate, user_id: int):
    db_transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.user_id == user_id
    ).first()
    
    if db_transaction:
        for key, value in transaction.dict(exclude_unset=True).items():
            setattr(db_transaction, key, value)
        db.commit()
        db.refresh(db_transaction)
    return db_transaction

def delete_transaction(db: Session, transaction_id: int, user_id: int):
    db_transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.user_id == user_id
    ).first()
    if db_transaction:
        db.delete(db_transaction)
        db.commit()
        return True
    return False

# Budget CRUD
def get_budgets(db: Session, user_id: int):
    return db.query(models.Budget).filter(models.Budget.user_id == user_id).all()

def create_budget(db: Session, budget: schemas.BudgetCreate, user_id: int):
    db_budget = models.Budget(**budget.dict(), user_id=user_id)
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

# Analytics
def get_monthly_summary(db: Session, user_id: int, month: str):
    transactions = db.query(
        models.Transaction.transaction_type,
        func.sum(models.Transaction.amount).label('total')
    ).filter(
        models.Transaction.user_id == user_id,
        func.strftime('%Y-%m', models.Transaction.date) == month
    ).group_by(models.Transaction.transaction_type).all()
    
    return {t.transaction_type: t.total or 0 for t in transactions}

def get_category_breakdown(db: Session, user_id: int, month: str = None):
    query = db.query(
        models.Transaction.category,
        func.sum(models.Transaction.amount).label('total')
    ).filter(
        models.Transaction.user_id == user_id,
        models.Transaction.transaction_type == 'expense'
    )
    
    if month:
        query = query.filter(func.strftime('%Y-%m', models.Transaction.date) == month)
    
    return query.group_by(models.Transaction.category).all()
