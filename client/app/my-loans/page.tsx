'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Loan } from '@/lib/types';
import { loanService } from '@/lib/loan.service';
import { useAuthStore } from '@/lib/store';
import { Card, CardBody } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { LoadingPage } from '@/components/ui/Loading';
import { formatDate } from '@/lib/utils';
import { BookOpen, Calendar, AlertCircle } from 'lucide-react';
import toast from 'react-hot-toast';

export default function MyLoansPage() {
  const router = useRouter();
  const { isAuthenticated, isLoading: authLoading } = useAuthStore();
  const [loans, setLoans] = useState<Loan[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [returningId, setReturningId] = useState<number | null>(null);
  const [filter, setFilter] = useState<string>('');

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login');
      return;
    }

    if (isAuthenticated) {
      fetchLoans();
    }
  }, [isAuthenticated, authLoading, filter]);

  const fetchLoans = async () => {
    try {
      setIsLoading(true);
      const response = await loanService.getMyLoans(filter);
      setLoans(response.results);
    } catch (error) {
      toast.error('Failed to fetch loans');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReturn = async (loanId: number) => {
    setReturningId(loanId);
    try {
      await loanService.returnBook(loanId);
      toast.success('Book returned successfully');
      fetchLoans();
    } catch (error: any) {
      toast.error(error.response?.data?.error || 'Failed to return book');
    } finally {
      setReturningId(null);
    }
  };

  if (authLoading || (!isAuthenticated && isLoading)) {
    return <LoadingPage />;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">My Loans</h1>
        <p className="text-lg text-gray-600">Manage your borrowed books</p>
      </div>

      {/* Filter Tabs */}
      <div className="flex space-x-2 mb-6 border-b border-gray-200">
        <button
          className={`px-4 py-2 font-medium transition-colors ${
            filter === '' ? 'border-b-2 border-primary-600 text-primary-600' : 'text-gray-600 hover:text-gray-900'
          }`}
          onClick={() => setFilter('')}
        >
          All Loans
        </button>
        <button
          className={`px-4 py-2 font-medium transition-colors ${
            filter === 'active' ? 'border-b-2 border-primary-600 text-primary-600' : 'text-gray-600 hover:text-gray-900'
          }`}
          onClick={() => setFilter('active')}
        >
          Active
        </button>
        <button
          className={`px-4 py-2 font-medium transition-colors ${
            filter === 'returned' ? 'border-b-2 border-primary-600 text-primary-600' : 'text-gray-600 hover:text-gray-900'
          }`}
          onClick={() => setFilter('returned')}
        >
          Returned
        </button>
        <button
          className={`px-4 py-2 font-medium transition-colors ${
            filter === 'overdue' ? 'border-b-2 border-primary-600 text-primary-600' : 'text-gray-600 hover:text-gray-900'
          }`}
          onClick={() => setFilter('overdue')}
        >
          Overdue
        </button>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-12">
          <LoadingPage />
        </div>
      ) : loans.length === 0 ? (
        <div className="text-center py-12">
          <BookOpen className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <p className="text-xl text-gray-600 mb-4">No loans found</p>
          <Button onClick={() => router.push('/books')}>
            Browse Books
          </Button>
        </div>
      ) : (
        <div className="space-y-4">
          {loans.map((loan) => (
            <Card key={loan.id}>
              <CardBody className="p-6">
                <div className="flex flex-col md:flex-row md:items-center md:justify-between">
                  <div className="flex-1">
                    <div className="flex items-start space-x-4">
                      <div className="flex-shrink-0">
                        <div className="w-16 h-20 bg-gradient-to-br from-primary-400 to-primary-600 rounded flex items-center justify-center">
                          <BookOpen className="h-8 w-8 text-white" />
                        </div>
                      </div>
                      
                      <div className="flex-1">
                        <h3 className="text-xl font-bold text-gray-900 mb-1">
                          {loan.book.title}
                        </h3>
                        <p className="text-gray-600 mb-3">by {loan.book.author}</p>
                        
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-sm">
                          <div className="flex items-center text-gray-600">
                            <Calendar className="h-4 w-4 mr-2" />
                            Borrowed: {formatDate(loan.borrow_date)}
                          </div>
                          <div className="flex items-center text-gray-600">
                            <Calendar className="h-4 w-4 mr-2" />
                            Due: {formatDate(loan.due_date)}
                          </div>
                          {loan.return_date && (
                            <div className="flex items-center text-green-600">
                              <Calendar className="h-4 w-4 mr-2" />
                              Returned: {formatDate(loan.return_date)}
                            </div>
                          )}
                        </div>

                        {loan.is_overdue && loan.status !== 'returned' && (
                          <div className="mt-3 flex items-center text-red-600">
                            <AlertCircle className="h-5 w-5 mr-2" />
                            <span className="font-semibold">
                              Overdue by {loan.days_overdue} days - Fine: ${loan.fine_amount}
                            </span>
                          </div>
                        )}

                        <div className="mt-3">
                          <span
                            className={`inline-block px-3 py-1 rounded-full text-xs font-semibold ${
                              loan.status === 'borrowed'
                                ? 'bg-blue-100 text-blue-800'
                                : loan.status === 'returned'
                                ? 'bg-green-100 text-green-800'
                                : 'bg-red-100 text-red-800'
                            }`}
                          >
                            {loan.status.toUpperCase()}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>

                  {loan.status !== 'returned' && (
                    <div className="mt-4 md:mt-0 md:ml-4">
                      <Button
                        variant="primary"
                        onClick={() => handleReturn(loan.id)}
                        isLoading={returningId === loan.id}
                      >
                        Return Book
                      </Button>
                    </div>
                  )}
                </div>
              </CardBody>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
