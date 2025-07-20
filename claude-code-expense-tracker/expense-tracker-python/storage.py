import json
import os
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from models import Expense, ExpenseCreate, ExpenseUpdate, ExpenseFilter, ExpenseSummary, ExpenseCategory
import uuid


class ExpenseStorage:
    def __init__(self, data_file: str = "expenses.json"):
        self.data_file = data_file
        self._load_data()
    
    def _load_data(self):
        """Load expenses from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.expenses = {
                        expense_id: Expense(**expense_data) 
                        for expense_id, expense_data in data.items()
                    }
            except (json.JSONDecodeError, ValueError):
                self.expenses = {}
        else:
            self.expenses = {}
    
    def _save_data(self):
        """Save expenses to JSON file"""
        data = {
            expense_id: expense.dict()
            for expense_id, expense in self.expenses.items()
        }
        
        # Convert datetime objects to ISO format strings
        for expense_data in data.values():
            expense_data['date'] = expense_data['date'].isoformat()
            expense_data['created_at'] = expense_data['created_at'].isoformat()
        
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def create_expense(self, expense_data: ExpenseCreate) -> Expense:
        """Create a new expense"""
        expense_id = str(uuid.uuid4())
        expense = Expense(id=expense_id, **expense_data.dict())
        self.expenses[expense_id] = expense
        self._save_data()
        return expense
    
    def get_expense(self, expense_id: str) -> Optional[Expense]:
        """Get expense by ID"""
        return self.expenses.get(expense_id)
    
    def get_all_expenses(self, filters: Optional[ExpenseFilter] = None) -> List[Expense]:
        """Get all expenses with optional filtering"""
        expenses = list(self.expenses.values())
        
        if filters:
            if filters.category:
                expenses = [e for e in expenses if e.category == filters.category]
            
            if filters.start_date:
                expenses = [e for e in expenses if e.date >= filters.start_date]
            
            if filters.end_date:
                expenses = [e for e in expenses if e.date <= filters.end_date]
            
            if filters.search_term:
                search_lower = filters.search_term.lower()
                expenses = [
                    e for e in expenses 
                    if search_lower in e.description.lower()
                ]
        
        # Sort by date (newest first)
        expenses.sort(key=lambda x: x.date, reverse=True)
        return expenses
    
    def update_expense(self, expense_id: str, update_data: ExpenseUpdate) -> Optional[Expense]:
        """Update an existing expense"""
        if expense_id not in self.expenses:
            return None
        
        expense = self.expenses[expense_id]
        update_dict = update_data.dict(exclude_unset=True)
        
        for field, value in update_dict.items():
            setattr(expense, field, value)
        
        self._save_data()
        return expense
    
    def delete_expense(self, expense_id: str) -> bool:
        """Delete an expense"""
        if expense_id in self.expenses:
            del self.expenses[expense_id]
            self._save_data()
            return True
        return False
    
    def get_summary(self) -> ExpenseSummary:
        """Get expense summary statistics"""
        expenses = list(self.expenses.values())
        
        if not expenses:
            return ExpenseSummary(
                total_expenses=0.0,
                monthly_expenses=0.0,
                expense_count=0,
                top_category=None,
                categories_breakdown={}
            )
        
        total_expenses = sum(e.amount for e in expenses)
        
        # Calculate monthly expenses (last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        monthly_expenses = sum(
            e.amount for e in expenses 
            if e.date >= thirty_days_ago
        )
        
        # Calculate category breakdown
        categories_breakdown = {}
        for category in ExpenseCategory:
            category_total = sum(
                e.amount for e in expenses 
                if e.category == category
            )
            if category_total > 0:
                categories_breakdown[category.value] = category_total
        
        # Find top category
        top_category = None
        if categories_breakdown:
            top_category = max(categories_breakdown.keys(), key=lambda k: categories_breakdown[k])
        
        return ExpenseSummary(
            total_expenses=total_expenses,
            monthly_expenses=monthly_expenses,
            expense_count=len(expenses),
            top_category=top_category,
            categories_breakdown=categories_breakdown
        )
    
    def export_to_csv(self) -> str:
        """Export expenses to CSV format"""
        expenses = self.get_all_expenses()
        
        if not expenses:
            return "No expenses to export"
        
        csv_lines = ["Date,Description,Category,Amount"]
        
        for expense in expenses:
            date_str = expense.date.strftime("%Y-%m-%d")
            # Escape commas in description
            description = expense.description.replace('"', '""')
            if ',' in description:
                description = f'"{description}"'
            
            csv_lines.append(f"{date_str},{description},{expense.category.value},{expense.amount:.2f}")
        
        return "\n".join(csv_lines)