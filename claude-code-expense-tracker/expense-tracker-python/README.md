# 💰 Expense Tracker

A modern, professional expense tracking web application built with FastAPI and NiceGUI. Track your personal finances with an intuitive, responsive interface.

## ✨ Features

### Core Functionality
- **Add Expenses**: Easy form with validation for amount, description, category, and date
- **View & Manage**: Clean list view with edit and delete capabilities
- **Filter & Search**: Filter by category, date range, and search by description
- **Dashboard Analytics**: Summary cards showing total spending, monthly expenses, and category breakdowns
- **Data Export**: Export expenses to CSV format
- **Data Persistence**: All data saved locally using JSON file storage

### Categories
- 🍔 Food
- 🚗 Transportation  
- 🎬 Entertainment
- 🛍️ Shopping
- 📄 Bills
- 📦 Other

### Design Features
- **Modern UI**: Clean, professional interface with gradient accents
- **Responsive Design**: Works seamlessly on desktop and mobile
- **Visual Feedback**: Hover effects, loading states, and notifications
- **Color-coded Categories**: Each category has its own distinctive color
- **Currency Formatting**: Proper formatting for all monetary values
- **Date Intelligence**: Smart date formatting (Today, Yesterday, etc.)

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- uv (Python package manager) - Install with: `curl -LsSf https://astral.sh/uv/install.sh | sh`

### Installation

1. **Clone or download the project files**
2. **Setup the project**:
   ```bash
   ./setup.sh
   ```
   
   Or manually:
   ```bash
   uv sync
   ```

3. **Run the application**:
   ```bash
   uv run python main.py
   ```
   
   Or use the convenience script:
   ```bash
   ./run_with_venv.py
   ```

4. **Access the application**:
   - Open your browser to: `http://localhost:8080`
   - The application will automatically open in your default browser

## 📖 How to Use

### Adding Expenses
1. Use the sidebar form on the left to add new expenses
2. Fill in:
   - **Amount**: The expense amount (must be positive)
   - **Description**: Brief description of the expense
   - **Category**: Select from predefined categories
   - **Date**: Date of the expense (defaults to today)
3. Click "Add Expense" to save

### Managing Expenses
- **View**: All expenses are displayed in the main area, sorted by date
- **Edit**: Click the edit icon (✏️) on any expense to modify it
- **Delete**: Click the delete icon (🗑️) to remove an expense (with confirmation)
- **Filter**: Use the category dropdown to filter by specific categories
- **Search**: Use the search box to find expenses by description

### Analytics Dashboard
The sidebar shows:
- **Total Expenses**: Sum of all expenses
- **This Month**: Expenses from the last 30 days
- **Total Count**: Number of expense entries
- **Top Category**: Category with highest spending
- **Category Breakdown**: Cards showing spending by category

### Exporting Data
- Click "Export CSV" to download your expenses as a CSV file
- File includes: Date, Description, Category, Amount

## 🏗️ Technical Architecture

### Backend (FastAPI)
- **REST API**: RESTful endpoints for all operations
- **Data Validation**: Pydantic models with comprehensive validation
- **Error Handling**: Proper HTTP status codes and error messages
- **File Storage**: JSON-based persistence with automatic backup

### Frontend (NiceGUI)
- **Reactive UI**: Real-time updates and responsive design
- **Modern Styling**: CSS3 with gradients, shadows, and animations
- **Component Architecture**: Modular, reusable UI components
- **State Management**: Global state with automatic refresh

### Key Endpoints
- `POST /api/expenses` - Create new expense
- `GET /api/expenses` - List expenses (with filtering)
- `PUT /api/expenses/{id}` - Update expense
- `DELETE /api/expenses/{id}` - Delete expense
- `GET /api/summary` - Get analytics summary
- `GET /api/export/csv` - Export to CSV

## 📁 Project Structure

```
expense-tracker-python/
├── main.py              # Main NiceGUI application
├── api.py               # FastAPI backend with endpoints
├── models.py            # Pydantic data models
├── storage.py           # Data persistence layer
├── run.py               # Simple run script
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── expenses.json       # Data storage (created automatically)
```

## 🔧 Configuration

### Ports
- **Frontend**: http://localhost:8080 (NiceGUI)
- **Backend API**: http://localhost:8001 (FastAPI)

### Data Storage
- Expenses are stored in `expenses.json` in the project directory
- File is created automatically on first use
- Data persists between application restarts

### Customization
You can easily customize:
- **Categories**: Modify `ExpenseCategory` enum in `models.py`
- **Colors**: Update `COLORS` and `get_category_color()` in `main.py`  
- **Validation**: Adjust validation rules in `models.py`
- **Storage**: Extend `ExpenseStorage` class for different backends

## 🐛 Troubleshooting

### Common Issues

**Dependencies not found**:
```bash
pip install -r requirements.txt
```

**Port already in use**:
- Change ports in `main.py` (line near `ui.run()`)
- Kill existing processes: `pkill -f "python main.py"`

**Data not persisting**:
- Check file permissions in project directory
- Ensure `expenses.json` can be created/modified

**Browser doesn't open automatically**:
- Manually navigate to `http://localhost:8080`
- Check if port 8080 is available

### Getting Help
1. Check the console output for error messages
2. Ensure all dependencies are installed correctly
3. Verify Python version is 3.8 or higher
4. Make sure ports 8080 and 8001 are available

## 🎯 Future Enhancements

Potential improvements for production use:
- **Database Integration**: PostgreSQL/SQLite instead of JSON
- **User Authentication**: Multi-user support with login
- **Advanced Analytics**: Charts, trends, and budget tracking
- **Receipt Upload**: Image upload and OCR processing
- **Mobile App**: Native mobile application
- **Data Sync**: Cloud synchronization across devices
- **Recurring Expenses**: Automatic recurring transaction handling
- **Budget Limits**: Category-wise budget setting and alerts

## 📄 License

This project is open source and available under the MIT License.

---

**Built with ❤️ using FastAPI and NiceGUI**