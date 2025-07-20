'use client';

import { useState, useEffect } from 'react';
import { Expense } from '@/types/expense';
import { storageUtils } from '@/lib/storage';
import { ExpenseList } from '@/components/ExpenseList';
import { ExpenseForm } from '@/components/ExpenseForm';
import { Modal } from '@/components/Modal';

export default function ExpensesPage() {
  const [expenses, setExpenses] = useState<Expense[]>([]);
  const [editingExpense, setEditingExpense] = useState<Expense | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    setExpenses(storageUtils.getExpenses());
  }, []);

  const handleEdit = (expense: Expense) => {
    setEditingExpense(expense);
    setIsModalOpen(true);
  };

  const handleDelete = (id: string) => {
    if (confirm('Are you sure you want to delete this expense?')) {
      storageUtils.deleteExpense(id);
      setExpenses(storageUtils.getExpenses());
    }
  };

  const handleExpenseUpdated = (_updatedExpense: Expense) => {
    setExpenses(storageUtils.getExpenses());
    setIsModalOpen(false);
    setEditingExpense(null);
  };

  const handleExport = () => {
    const csvContent = storageUtils.exportToCSV(expenses);
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'expenses.csv';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Expenses</h1>
        <p className="text-gray-600 mt-2">Manage and track all your expenses</p>
      </div>

      <ExpenseList
        expenses={expenses}
        onEdit={handleEdit}
        onDelete={handleDelete}
        onExport={handleExport}
      />

      <Modal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          setEditingExpense(null);
        }}
        title="Edit Expense"
      >
        {editingExpense && (
          <ExpenseForm
            expense={editingExpense}
            onSubmit={handleExpenseUpdated}
            onCancel={() => {
              setIsModalOpen(false);
              setEditingExpense(null);
            }}
          />
        )}
      </Modal>
    </div>
  );
}