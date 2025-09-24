from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict
import crud, models
from database import get_db
from auth import get_current_user

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/monthly-summary/{month}")
def get_monthly_summary(
    month: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    summary = crud.get_monthly_summary(db, user_id=current_user.id, month=month)
    return {
        "month": month,
        "income": summary.get("income", 0),
        "expense": summary.get("expense", 0),
        "balance": summary.get("income", 0) - summary.get("expense", 0)
    }

@router.get("/category-breakdown")
def get_category_breakdown(
    month: str = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    breakdown = crud.get_category_breakdown(db, user_id=current_user.id, month=month)
    return [{"category": cat, "total": total} for cat, total in﻿ 
