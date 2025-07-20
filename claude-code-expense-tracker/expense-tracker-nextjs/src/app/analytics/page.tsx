'use client';

import { useState, useEffect } from 'react';
import { storageUtils } from '@/lib/storage';
import { calculateExpenseSummary, getCategoryData } from '@/lib/utils';
import { Expense } from '@/types/expense';
import { SpendingChart } from '@/components/SpendingChart';
import { formatCurrency } from '@/lib/utils';
import { TrendingUp, Calendar, DollarSign } from 'lucide-react';
import { format, startOfMonth, endOfMonth, eachMonthOfInterval, subMonths } from 'date-fns';

export default function AnalyticsPage() {
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
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-8"></div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {[1, 2].map((i) => (
              <div key={i} className="bg-gray-200 h-64 rounded-lg"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  const summary = calculateExpenseSummary(expenses);
  const categoryData = getCategoryData(expenses);

  // Calculate monthly trends
  const now = new Date();
  const last6Months = eachMonthOfInterval({
    start: subMonths(now, 5),
    end: now,
  });

  const monthlyData = last6Months.map(month => {
    const monthStart = startOfMonth(month);
    const monthEnd = endOfMonth(month);
    
    const monthExpenses = expenses.filter(expense => {
      const expenseDate = new Date(expense.date);
      return expenseDate >= monthStart && expenseDate <= monthEnd;
    });
    
    const total = monthExpenses.reduce((sum, expense) => sum + expense.amount, 0);
    
    return {
      month: format(month, 'MMM yyyy'),
      total,
      count: monthExpenses.length,
    };
  });

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Analytics</h1>
        <p className="text-gray-600 mt-2">Detailed insights into your spending patterns</p>
      </div>

      {expenses.length === 0 ? (
        <div className="text-center py-12">
          <div className="bg-white rounded-lg shadow-sm p-12">
            <TrendingUp className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h2 className="text-xl font-semibold text-gray-900 mb-2">No Data Available</h2>
            <p className="text-gray-600">Add some expenses to see analytics and insights.</p>
          </div>
        </div>
      ) : (
        <div className="space-y-8">
          {/* Charts */}
          <SpendingChart summary={summary} />

          {/* Monthly Trends */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Monthly Spending Trend</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
              {monthlyData.map((month, index) => (
                <div key={index} className="text-center p-4 border border-gray-200 rounded-md">
                  <p className="text-sm text-gray-600 mb-1">{month.month}</p>
                  <p className="text-lg font-semibold text-gray-900">{formatCurrency(month.total)}</p>
                  <p className="text-xs text-gray-500">{month.count} expenses</p>
                </div>
              ))}
            </div>
          </div>

          {/* Category Details */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Category Analysis</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {categoryData.map((category) => (
                <div key={category.category} className="p-4 border border-gray-200 rounded-md">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-medium text-gray-900">{category.category}</h4>
                    <span className="text-sm text-gray-500">{category.count} expenses</span>
                  </div>
                  <p className="text-2xl font-bold text-gray-900">
                    {formatCurrency(category.total)}
                  </p>
                  <p className="text-sm text-gray-600 mt-1">
                    Avg: {formatCurrency(category.total / category.count)}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Summary Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center">
                <DollarSign className="h-10 w-10 text-green-600 bg-green-100 rounded-full p-2" />
                <div className="ml-4">
                  <p className="text-sm text-gray-600">Average Expense</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {formatCurrency(summary.totalSpending / expenses.length || 0)}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center">
                <Calendar className="h-10 w-10 text-blue-600 bg-blue-100 rounded-full p-2" />
                <div className="ml-4">
                  <p className="text-sm text-gray-600">Total Expenses</p>
                  <p className="text-2xl font-bold text-gray-900">{expenses.length}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center">
                <TrendingUp className="h-10 w-10 text-purple-600 bg-purple-100 rounded-full p-2" />
                <div className="ml-4">
                  <p className="text-sm text-gray-600">Categories Used</p>
                  <p className="text-2xl font-bold text-gray-900">{categoryData.length}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}