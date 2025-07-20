'use client';

import { useState, useEffect } from 'react';
import { storageUtils } from '@/lib/storage';
import { calculateExpenseSummary } from '@/lib/utils';
import { Expense } from '@/types/expense';
import { SummaryCards } from '@/components/SummaryCards';
import { SpendingChart } from '@/components/SpendingChart';
import { RecentExpenses } from '@/components/RecentExpenses';
import Link from 'next/link';
import { Plus } from 'lucide-react';

export default function Dashboard() {
  const [expenses, setExpenses] = useState<Expense[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadExpenses = () => {
      const data = storageUtils.getExpenses();
      setExpenses(data);
      setIsLoading(false);
    };

    loadExpenses();
  }, []);

  if (isLoading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="bg-gray-200 h-24 rounded-lg"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  const summary = calculateExpenseSummary(expenses);

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-2">Overview of your expense tracking</p>
        </div>
        <Link
          href="/add"
          className="flex items-center space-x-2 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <Plus className="h-4 w-4" />
          <span>Add Expense</span>
        </Link>
      </div>

      {/* Summary Cards */}
      <div className="mb-8">
        <SummaryCards summary={summary} />
      </div>

      {expenses.length === 0 ? (
        /* Empty State */
        <div className="text-center py-12">
          <div className="bg-white rounded-lg shadow-sm p-12">
            <div className="max-w-md mx-auto">
              <div className="text-6xl mb-4">💰</div>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                Welcome to Expense Tracker
              </h2>
              <p className="text-gray-600 mb-6">
                Start tracking your expenses to get insights into your spending habits.
                Add your first expense to see your financial overview.
              </p>
              <Link
                href="/add"
                className="inline-flex items-center space-x-2 bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <Plus className="h-5 w-5" />
                <span>Add Your First Expense</span>
              </Link>
            </div>
          </div>
        </div>
      ) : (
        /* Dashboard Content */
        <div className="space-y-8">
          {/* Charts */}
          <SpendingChart summary={summary} />

          {/* Recent Expenses */}
          <RecentExpenses expenses={summary.recentExpenses} />
        </div>
      )}
    </div>
  );
}