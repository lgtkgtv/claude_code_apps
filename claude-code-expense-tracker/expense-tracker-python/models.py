from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from enum import Enum


class ExpenseCategory(str, Enum):
    FOOD = "Food"
    TRANSPORTATION = "Transportation"
    ENTERTAINMENT = "Entertainment"
    SHOPPING = "Shopping"
    BILLS = "Bills"
    OTHER = "Other"


class ExpenseCreate(BaseModel):
    amount: float = Field(..., gt=0, description="Expense amount must be positive")
    description: str = Field(..., min_length=1, max_length=200, description="Expense description")
    category: ExpenseCategory
    date: datetime
    
    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        if v > 999999.99:
            raise ValueError('Amount too large')
        return round(v, 2)
    
    @validator('description')
    def validate_description(cls, v):
        return v.strip()


class Expense(ExpenseCreate):
    id: str
    created_at: datetime = Field(default_factory=datetime.now)


class ExpenseUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    description: Optional[str] = Field(None, min_length=1, max_length=200)
    category: Optional[ExpenseCategory] = None
    date: Optional[datetime] = None
    
    @validator('amount')
    def validate_amount(cls, v):
        if v is not None:
            if v <= 0:
                raise ValueError('Amount must be positive')
            if v > 999999.99:
                raise ValueError('Amount too large')
            return round(v, 2)
        return v
    
    @validator('description')
    def validate_description(cls, v):
        if v is not None:
            return v.strip()
        return v


class ExpenseFilter(BaseModel):
    category: Optional[ExpenseCategory] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    search_term: Optional[str] = None


class ExpenseSummary(BaseModel):
    total_expenses: float
    monthly_expenses: float
    expense_count: int
    top_category: Optional[str]
    categories_breakdown: dict[str, float]