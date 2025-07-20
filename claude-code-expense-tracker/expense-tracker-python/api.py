from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import Response
from typing import List, Optional
from datetime import datetime
from models import (
    Expense, ExpenseCreate, ExpenseUpdate, ExpenseFilter, 
    ExpenseSummary, ExpenseCategory
)
from storage import ExpenseStorage

app = FastAPI(
    title="Expense Tracker API",
    description="A modern expense tracking application API",
    version="1.0.0"
)

# Initialize storage
storage = ExpenseStorage()


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Expense Tracker API is running"}


@app.post("/api/expenses", response_model=Expense)
async def create_expense(expense: ExpenseCreate):
    """Create a new expense"""
    try:
        return storage.create_expense(expense)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/expenses", response_model=List[Expense])
async def get_expenses(
    category: Optional[ExpenseCategory] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    search_term: Optional[str] = Query(None)
):
    """Get all expenses with optional filtering"""
    filters = ExpenseFilter(
        category=category,
        start_date=start_date,
        end_date=end_date,
        search_term=search_term
    )
    return storage.get_all_expenses(filters)


@app.get("/api/expenses/{expense_id}", response_model=Expense)
async def get_expense(expense_id: str):
    """Get a specific expense by ID"""
    expense = storage.get_expense(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@app.put("/api/expenses/{expense_id}", response_model=Expense)
async def update_expense(expense_id: str, expense_update: ExpenseUpdate):
    """Update an existing expense"""
    try:
        updated_expense = storage.update_expense(expense_id, expense_update)
        if not updated_expense:
            raise HTTPException(status_code=404, detail="Expense not found")
        return updated_expense
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/api/expenses/{expense_id}")
async def delete_expense(expense_id: str):
    """Delete an expense"""
    if not storage.delete_expense(expense_id):
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "Expense deleted successfully"}


@app.get("/api/summary", response_model=ExpenseSummary)
async def get_summary():
    """Get expense summary and analytics"""
    return storage.get_summary()


@app.get("/api/categories", response_model=List[str])
async def get_categories():
    """Get all available expense categories"""
    return [category.value for category in ExpenseCategory]


@app.get("/api/export/csv")
async def export_csv():
    """Export expenses to CSV"""
    csv_content = storage.export_to_csv()
    
    if csv_content == "No expenses to export":
        raise HTTPException(status_code=404, detail="No expenses to export")
    
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=expenses.csv"}
    )