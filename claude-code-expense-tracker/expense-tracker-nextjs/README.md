# 💰 Expense Tracker

A modern, professional expense tracking web application built with Next.js 14, TypeScript, and Tailwind CSS. Track your personal finances with an intuitive interface, powerful analytics, and comprehensive expense management features.

![Expense Tracker](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?style=for-the-badge&logo=typescript)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-3-38bdf8?style=for-the-badge&logo=tailwind-css)

## 🚀 Features

### Core Functionality
- ✅ **Add Expenses**: Quick and easy expense entry with validation
- ✅ **Expense Management**: View, edit, and delete expenses
- ✅ **Smart Filtering**: Filter by category, date range, and search terms
- ✅ **Data Export**: Export expenses to CSV format
- ✅ **Responsive Design**: Works seamlessly on desktop and mobile

### Analytics & Insights
- 📊 **Dashboard Overview**: Summary cards with key metrics
- 📈 **Visual Charts**: Pie charts and bar charts for spending analysis
- 📅 **Monthly Trends**: Track spending patterns over time
- 🎯 **Category Breakdown**: Detailed analysis by expense category

### Categories
- 🍔 Food
- 🚗 Transportation
- 🎮 Entertainment
- 🛒 Shopping
- 💡 Bills
- 📦 Other

## 🛠️ Tech Stack

- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **Icons**: Lucide React
- **Date Handling**: date-fns
- **Data Storage**: localStorage (client-side)

## 📦 Installation

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd expense-tracker
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```

4. **Open your browser** and navigate to:
   ```
   http://localhost:3000
   ```

## 🚀 Available Scripts

```bash
# Development
npm run dev          # Start development server with Turbopack

# Production
npm run build        # Build for production
npm run start        # Start production server

# Code Quality
npm run lint         # Run ESLint
```

## 📱 Usage Guide

### Getting Started
1. **Dashboard**: View your expense overview and key metrics
2. **Add Expense**: Click "Add Expense" to create new entries
3. **Manage Expenses**: View, edit, or delete expenses in the Expenses page
4. **Analytics**: Explore detailed insights and trends

### Adding an Expense
1. Navigate to "Add Expense" or click the "+" button
2. Fill in the required fields:
   - **Amount**: Enter the expense amount (e.g., 25.99)
   - **Category**: Select from predefined categories
   - **Description**: Add details about the expense
   - **Date**: Choose the expense date
3. Click "Add Expense" to save

### Managing Expenses
- **View**: All expenses are displayed in a sortable table
- **Search**: Use the search bar to find specific expenses
- **Filter**: Filter by category or date range
- **Edit**: Click the edit icon to modify an expense
- **Delete**: Click the trash icon to remove an expense
- **Export**: Download your expenses as a CSV file

### Analytics Features
- **Summary Cards**: Total spending, monthly spending, top category, and recent count
- **Visual Charts**: Pie chart for category distribution, bar chart for amounts
- **Monthly Trends**: Track spending patterns over the last 6 months
- **Category Analysis**: Detailed breakdown with averages and totals

## 🏗️ Project Structure

```
expense-tracker/
├── src/
│   ├── app/                    # Next.js app router pages
│   │   ├── add/               # Add expense page
│   │   ├── analytics/         # Analytics page
│   │   ├── expenses/          # Expenses management page
│   │   ├── layout.tsx         # Root layout
│   │   └── page.tsx           # Dashboard/home page
│   ├── components/            # Reusable React components
│   │   ├── ExpenseForm.tsx    # Form for adding/editing expenses
│   │   ├── ExpenseList.tsx    # List and filter expenses
│   │   ├── Modal.tsx          # Modal component
│   │   ├── Navigation.tsx     # Navigation bar
│   │   ├── RecentExpenses.tsx # Recent expenses widget
│   │   ├── SpendingChart.tsx  # Charts for analytics
│   │   └── SummaryCards.tsx   # Dashboard summary cards
│   ├── lib/                   # Utility functions
│   │   ├── storage.ts         # localStorage utilities
│   │   └── utils.ts           # Helper functions and calculations
│   └── types/                 # TypeScript type definitions
│       └── expense.ts         # Expense-related types
├── public/                    # Static assets
├── package.json              # Dependencies and scripts
└── README.md                 # This file
```

## 🎨 Design System

The application uses a modern, professional design with:

- **Color Palette**: Blue primary (#3B82F6), with semantic colors for categories
- **Typography**: Clean, readable fonts with proper hierarchy
- **Spacing**: Consistent spacing using Tailwind's spacing scale
- **Components**: Reusable, accessible UI components
- **Responsive**: Mobile-first design that works on all screen sizes

## 💾 Data Storage

The application uses browser localStorage for data persistence:

- **Advantages**: No backend required, instant access, offline capability
- **Data Format**: JSON serialization of expense objects
- **Backup**: Use the export feature to create CSV backups
- **Privacy**: All data stays on your device

## 🔮 Future Enhancements

Potential features for future development:

- 🔐 User authentication and cloud storage
- 📱 Progressive Web App (PWA) capabilities
- 🎯 Budget tracking and alerts
- 📊 Advanced analytics and reporting
- 🔄 Data import from bank statements
- 📧 Email reports and summaries
- 🌙 Dark mode support
- 💱 Multi-currency support

## 🤝 Contributing

This is a demo application, but contributions are welcome:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature/new-feature`
5. Submit a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

If you encounter any issues or have questions:

1. Check the browser console for error messages
2. Ensure you're using a modern browser with localStorage support
3. Try clearing your browser cache and localStorage
4. Create an issue in the repository for bugs or feature requests

## 🎯 Testing Checklist

To verify all features work correctly:

### Basic Functionality
- [ ] Add a new expense with all fields
- [ ] View expenses in the list
- [ ] Edit an existing expense
- [ ] Delete an expense
- [ ] Search for expenses
- [ ] Filter by category and date

### Analytics
- [ ] View dashboard summary cards
- [ ] Check pie chart displays correctly
- [ ] Verify bar chart shows category data
- [ ] Review monthly trends
- [ ] Examine category analysis

### Export/Import
- [ ] Export expenses to CSV
- [ ] Verify CSV format and data accuracy

### Responsive Design
- [ ] Test on mobile devices
- [ ] Verify tablet layout
- [ ] Check desktop experience
- [ ] Test navigation on different screen sizes

---

**Built with ❤️ using Next.js 14, TypeScript, and Tailwind CSS**