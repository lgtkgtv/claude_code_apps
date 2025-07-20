export type ExpenseCategory = 
  | 'Food'
  | 'Transportation'
  | 'Entertainment'
  | 'Shopping'
  | 'Bills'
  | 'Other';

export interface Expense {
  id: string;
  amount: number;
  category: ExpenseCategory;
  description: string;
  date: string; // ISO string format
  createdAt: string; // ISO string format
  updatedAt: string; // ISO string format
}

export interface ExpenseFilters {
  category?: ExpenseCategory;
  startDate?: string;
  endDate?: string;
  searchQuery?: string;
}

export interface ExpenseSummary {
  totalSpending: number;
  monthlySpending: number;
  topCategories: Array<{
    category: ExpenseCategory;
    total: number;
    percentage: number;
  }>;
  recentExpenses: Expense[];
}

export interface CategoryData {
  category: ExpenseCategory;
  total: number;
  count: number;
}