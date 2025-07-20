'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { ExpenseForm } from '@/components/ExpenseForm';
import { Expense } from '@/types/expense';
import { CheckCircle } from 'lucide-react';

export default function AddExpensePage() {
  const router = useRouter();
  const [showSuccess, setShowSuccess] = useState(false);

  const handleExpenseAdded = (_expense: Expense) => {
    setShowSuccess(true);
    setTimeout(() => {
      setShowSuccess(false);
      router.push('/expenses');
    }, 2000);
  };

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Add New Expense</h1>
        
        {showSuccess && (
          <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-md flex items-center space-x-2">
            <CheckCircle className="h-5 w-5 text-green-600" />
            <span className="text-green-800">Expense added successfully! Redirecting...</span>
          </div>
        )}
        
        <ExpenseForm onSubmit={handleExpenseAdded} />
      </div>
    </div>
  );
}