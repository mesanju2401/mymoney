from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from typing import Optional, List

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Transaction schemas
class TransactionBase(BaseModel):
    amount: float
    category: str
    description: Optional[str] = None
    transaction_type: str
    date: Optional[datetime] = None
    
    @validator('transaction_type')
    def validate_type(cls, v):
        if v not in ['income', 'expense']:
            raise ValueError('Transaction type must be income or expense')
        return v

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None
    transaction_type: Optional[str] = None
    date: Optional[datetime] = None

class Transaction(TransactionBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True

# Budget schemas
class BudgetBase(BaseModel):
    category: str
    amount: float
    month: str

class BudgetCreate(BudgetBase):
    pass

class Budget(BudgetBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True

# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None﻿ 
