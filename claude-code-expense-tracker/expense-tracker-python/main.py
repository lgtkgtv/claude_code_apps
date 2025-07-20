#!/usr/bin/env python3
from nicegui import ui, app, run
from datetime import datetime, date, timedelta
from typing import Optional, List
import asyncio
import threading
import uvicorn
from contextlib import asynccontextmanager
import requests
import json

from models import ExpenseCreate, ExpenseUpdate, ExpenseCategory
from storage import ExpenseStorage

# Initialize storage
storage = ExpenseStorage()

# API base URL
API_BASE_URL = "http://localhost:8001/api"

# Global state
current_expenses = []
current_summary = None
selected_expense_id = None
edit_mode = False

# Color scheme
COLORS = {
    'primary': '#2563eb',
    'secondary': '#64748b',
    'success': '#059669',
    'danger': '#dc2626',
    'warning': '#d97706',
    'light': '#f8fafc',
    'dark': '#1e293b',
    'border': '#e2e8f0'
}

async def start_fastapi():
    """Start FastAPI server in background"""
    config = uvicorn.Config(
        "api:app",
        host="127.0.0.1",
        port=8001,
        log_level="warning"
    )
    server = uvicorn.Server(config)
    await server.serve()

def start_fastapi_thread():
    """Start FastAPI in a separate thread"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_fastapi())

def fetch_expenses():
    """Fetch expenses from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/expenses")
        if response.status_code == 200:
            return response.json()
        return []
    except requests.exceptions.RequestException:
        return storage.get_all_expenses()

def fetch_summary():
    """Fetch summary from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/summary")
        if response.status_code == 200:
            return response.json()
        return storage.get_summary().dict()
    except requests.exceptions.RequestException:
        return storage.get_summary().dict()

def format_currency(amount: float) -> str:
    """Format amount as currency"""
    return f"${amount:,.2f}"

def format_date(date_obj) -> str:
    """Format date for display"""
    if isinstance(date_obj, str):
        date_obj = datetime.fromisoformat(date_obj.replace('Z', '+00:00'))
    elif isinstance(date_obj, datetime):
        pass
    else:
        return str(date_obj)
    
    today = datetime.now().date()
    expense_date = date_obj.date()
    
    if expense_date == today:
        return "Today"
    elif expense_date == today - timedelta(days=1):
        return "Yesterday"
    else:
        return expense_date.strftime("%b %d, %Y")

def get_category_color(category: str) -> str:
    """Get color for category"""
    colors = {
        'Food': '#f59e0b',
        'Transportation': '#3b82f6',
        'Entertainment': '#8b5cf6',
        'Shopping': '#ec4899',
        'Bills': '#ef4444',
        'Other': '#6b7280'
    }
    return colors.get(category, '#6b7280')

async def refresh_data():
    """Refresh all data"""
    global current_expenses, current_summary
    current_expenses = fetch_expenses()
    current_summary = fetch_summary()

@ui.page('/')
async def main_page():
    """Main application page"""
    await refresh_data()
    
    # Custom CSS for modern design
    ui.add_head_html('''
    <style>
        .expense-card {
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        }
        .expense-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }
        .summary-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .category-badge {
            border-radius: 12px;
            padding: 4px 12px;
            font-size: 0.75rem;
            font-weight: 600;
            color: white;
        }
        .add-button {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            z-index: 1000;
        }
        .sidebar {
            background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
        }
        .main-content {
            background: #fafbfc;
            min-height: 100vh;
        }
    </style>
    ''')
    
    with ui.row().classes('w-full min-h-screen'):
        # Sidebar
        with ui.column().classes('w-80 sidebar p-6 shadow-lg'):
            ui.label('💰 Expense Tracker').classes('text-2xl font-bold text-gray-800 mb-6')
            
            # Summary Cards
            with ui.card().classes('summary-card mb-4'):
                with ui.card_section():
                    ui.label('Total Expenses').classes('text-sm text-white opacity-80')
                    ui.label(format_currency(current_summary.get('total_expenses', 0))).classes('text-2xl font-bold text-white')
            
            with ui.card().classes('mb-4'):
                with ui.card_section():
                    ui.label('This Month').classes('text-sm text-gray-600')
                    ui.label(format_currency(current_summary.get('monthly_expenses', 0))).classes('text-xl font-bold text-gray-800')
            
            with ui.card().classes('mb-4'):
                with ui.card_section():
                    ui.label('Total Count').classes('text-sm text-gray-600')
                    ui.label(str(current_summary.get('expense_count', 0))).classes('text-xl font-bold text-gray-800')
            
            if current_summary.get('top_category'):
                with ui.card().classes('mb-6'):
                    with ui.card_section():
                        ui.label('Top Category').classes('text-sm text-gray-600')
                        ui.label(current_summary['top_category']).classes('text-lg font-bold text-gray-800')
            
            # Add Expense Form
            ui.separator().classes('my-4')
            ui.label('Add New Expense').classes('text-lg font-semibold text-gray-800 mb-4')
            
            with ui.card().classes('p-4'):
                amount_input = ui.number('Amount', placeholder='0.00', format='%.2f').classes('mb-3')
                description_input = ui.input('Description', placeholder='Enter description').classes('mb-3')
                category_select = ui.select(
                    options=[cat.value for cat in ExpenseCategory],
                    label='Category',
                    value='Other'
                ).classes('mb-3')
                ui.label('Date').classes('text-sm font-medium text-gray-700 mb-1')
                date_input = ui.date(value=date.today().strftime('%Y-%m-%d')).classes('mb-4')
                
                async def add_expense():
                    if not amount_input.value or amount_input.value <= 0:
                        ui.notify('Please enter a valid amount', type='negative')
                        return
                    if not description_input.value or not description_input.value.strip():
                        ui.notify('Please enter a description', type='negative')
                        return
                    
                    try:
                        expense_data = {
                            'amount': float(amount_input.value),
                            'description': description_input.value.strip(),
                            'category': category_select.value,
                            'date': datetime.fromisoformat(date_input.value).isoformat()
                        }
                        
                        response = requests.post(f"{API_BASE_URL}/expenses", json=expense_data)
                        
                        if response.status_code == 200:
                            ui.notify('Expense added successfully!', type='positive')
                            amount_input.value = None
                            description_input.value = ''
                            category_select.value = 'Other'
                            date_input.value = date.today().strftime('%Y-%m-%d')
                            await refresh_data()
                            expense_list.refresh()
                            summary_container.refresh()
                        else:
                            ui.notify('Failed to add expense', type='negative')
                    except Exception as e:
                        ui.notify(f'Error: {str(e)}', type='negative')
                
                ui.button('Add Expense', on_click=add_expense).props('color=primary').classes('w-full')
        
        # Main Content Area
        with ui.column().classes('flex-1 main-content p-6'):
            # Header
            with ui.row().classes('w-full justify-between items-center mb-6'):
                ui.label('Recent Expenses').classes('text-2xl font-bold text-gray-800')
                
                # Filters
                with ui.row().classes('gap-2'):
                    category_filter = ui.select(
                        options=['All'] + [cat.value for cat in ExpenseCategory],
                        label='Filter by Category',
                        value='All'
                    ).classes('w-48')
                    
                    search_input = ui.input('Search', placeholder='Search expenses...').classes('w-64')
                    
                    export_button = ui.button('Export CSV', icon='download').props('outlined color=secondary')
                    
                    async def export_csv():
                        try:
                            response = requests.get(f"{API_BASE_URL}/export/csv")
                            if response.status_code == 200:
                                ui.download(response.content, 'expenses.csv')
                                ui.notify('Expenses exported successfully!', type='positive')
                            else:
                                ui.notify('No expenses to export', type='warning')
                        except Exception as e:
                            ui.notify(f'Export failed: {str(e)}', type='negative')
                    
                    export_button.on_click(export_csv)
            
            # Summary refresh container
            @ui.refreshable
            def summary_container():
                if current_summary and current_summary.get('categories_breakdown'):
                    with ui.row().classes('w-full gap-4 mb-6'):
                        for category, amount in current_summary['categories_breakdown'].items():
                            with ui.card().classes('p-4 flex-1'):
                                with ui.row().classes('items-center justify-between'):
                                    with ui.column():
                                        ui.label(category).classes('text-sm text-gray-600')
                                        ui.label(format_currency(amount)).classes('text-lg font-bold')
                                    ui.icon('category').style(f'color: {get_category_color(category)}; font-size: 2rem;')
            
            summary_container()
            
            # Expense List
            @ui.refreshable
            def expense_list():
                filtered_expenses = current_expenses
                
                # Apply filters
                if category_filter.value and category_filter.value != 'All':
                    filtered_expenses = [e for e in filtered_expenses if e.get('category') == category_filter.value]
                
                if search_input.value:
                    search_term = search_input.value.lower()
                    filtered_expenses = [
                        e for e in filtered_expenses 
                        if search_term in e.get('description', '').lower()
                    ]
                
                if not filtered_expenses:
                    with ui.card().classes('p-8 text-center'):
                        ui.icon('receipt_long').classes('text-6xl text-gray-400 mb-4')
                        ui.label('No expenses found').classes('text-xl text-gray-600 mb-2')
                        ui.label('Add your first expense using the form on the left').classes('text-gray-500')
                else:
                    for expense in filtered_expenses:
                        with ui.card().classes('expense-card mb-3 p-4'):
                            with ui.row().classes('w-full justify-between items-center'):
                                with ui.column().classes('flex-1'):
                                    with ui.row().classes('items-center gap-2 mb-2'):
                                        ui.label(expense.get('description', '')).classes('text-lg font-semibold text-gray-800')
                                        ui.html(f'''
                                            <span class="category-badge" style="background-color: {get_category_color(expense.get('category', 'Other'))}">
                                                {expense.get('category', 'Other')}
                                            </span>
                                        ''')
                                    
                                    with ui.row().classes('items-center gap-4 text-sm text-gray-600'):
                                        ui.icon('schedule').classes('text-base')
                                        ui.label(format_date(expense.get('date', '')))
                                
                                with ui.column().classes('items-end'):
                                    ui.label(format_currency(expense.get('amount', 0))).classes('text-xl font-bold text-gray-800 mb-2')
                                    
                                    with ui.row().classes('gap-1'):
                                        edit_btn = ui.button(icon='edit', on_click=lambda e=expense: edit_expense(e)).props('size=sm outlined color=primary')
                                        delete_btn = ui.button(icon='delete', on_click=lambda e=expense: delete_expense(e)).props('size=sm outlined color=negative')
            
            expense_list()
            
            # Filter change handlers
            async def on_filter_change():
                expense_list.refresh()
            
            category_filter.on('update:model-value', lambda: on_filter_change())
            search_input.on('update:model-value', lambda: on_filter_change())

async def edit_expense(expense):
    """Edit expense dialog"""
    with ui.dialog() as dialog, ui.card().classes('w-96'):
        ui.label('Edit Expense').classes('text-lg font-semibold mb-4')
        
        amount_input = ui.number('Amount', value=expense.get('amount', 0), format='%.2f').classes('mb-3')
        description_input = ui.input('Description', value=expense.get('description', '')).classes('mb-3')
        category_select = ui.select(
            options=[cat.value for cat in ExpenseCategory],
            label='Category',
            value=expense.get('category', 'Other')
        ).classes('mb-3')
        
        expense_date = expense.get('date', '')
        if isinstance(expense_date, str):
            expense_date = datetime.fromisoformat(expense_date.replace('Z', '+00:00')).date()
        ui.label('Date').classes('text-sm font-medium text-gray-700 mb-1')
        date_input = ui.date(value=expense_date.strftime('%Y-%m-%d') if expense_date else date.today().strftime('%Y-%m-%d')).classes('mb-4')
        
        with ui.row().classes('justify-end gap-2'):
            ui.button('Cancel', on_click=dialog.close).props('outlined')
            
            async def save_changes():
                try:
                    update_data = {
                        'amount': float(amount_input.value),
                        'description': description_input.value.strip(),
                        'category': category_select.value,
                        'date': datetime.fromisoformat(date_input.value).isoformat()
                    }
                    
                    response = requests.put(f"{API_BASE_URL}/expenses/{expense['id']}", json=update_data)
                    
                    if response.status_code == 200:
                        ui.notify('Expense updated successfully!', type='positive')
                        await refresh_data()
                        expense_list.refresh()
                        summary_container.refresh()
                        dialog.close()
                    else:
                        ui.notify('Failed to update expense', type='negative')
                except Exception as e:
                    ui.notify(f'Error: {str(e)}', type='negative')
            
            ui.button('Save', on_click=save_changes).props('color=primary')
    
    dialog.open()

async def delete_expense(expense):
    """Delete expense with confirmation"""
    with ui.dialog() as dialog, ui.card().classes('w-80'):
        ui.label('Confirm Delete').classes('text-lg font-semibold mb-4')
        ui.label(f'Are you sure you want to delete "{expense.get("description", "")}"?').classes('mb-4')
        
        with ui.row().classes('justify-end gap-2'):
            ui.button('Cancel', on_click=dialog.close).props('outlined')
            
            async def confirm_delete():
                try:
                    response = requests.delete(f"{API_BASE_URL}/expenses/{expense['id']}")
                    
                    if response.status_code == 200:
                        ui.notify('Expense deleted successfully!', type='positive')
                        await refresh_data()
                        expense_list.refresh()
                        summary_container.refresh()
                        dialog.close()
                    else:
                        ui.notify('Failed to delete expense', type='negative')
                except Exception as e:
                    ui.notify(f'Error: {str(e)}', type='negative')
            
            ui.button('Delete', on_click=confirm_delete).props('color=negative')
    
    dialog.open()

if __name__ in {"__main__", "__mp_main__"}:
    # Start FastAPI server in background thread
    fastapi_thread = threading.Thread(target=start_fastapi_thread, daemon=True)
    fastapi_thread.start()
    
    # Give FastAPI time to start
    import time
    time.sleep(2)
    
    # Run NiceGUI
    ui.run(
        title='Expense Tracker',
        favicon='💰',
        port=8080,
        show=True,
        reload=False
    )