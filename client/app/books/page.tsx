'use client';

import React, { useState, useEffect } from 'react';
import { Book, BookFilters } from '@/lib/types';
import { bookService } from '@/lib/book.service';
import { loanService } from '@/lib/loan.service';
import { BookCard } from '@/components/BookCard';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { LoadingSpinner } from '@/components/ui/Loading';
import { Modal } from '@/components/ui/Modal';
import { useAuthStore } from '@/lib/store';
import { Search, Filter } from 'lucide-react';
import toast from 'react-hot-toast';
import { formatDate } from '@/lib/utils';

export default function BooksPage() {
  const { isAuthenticated, user } = useAuthStore();
  const [books, setBooks] = useState<Book[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [borrowingId, setBorrowingId] = useState<number | null>(null);
  const [selectedBook, setSelectedBook] = useState<Book | null>(null);
  const [showDetails, setShowDetails] = useState(false);
  const [categories, setCategories] = useState<string[]>([]);
  
  const [filters, setFilters] = useState<BookFilters>({
    search: '',
    category: '',
    available: undefined,
    page: 1,
    page_size: 12,
  });

  const [pagination, setPagination] = useState({
    count: 0,
    next: null as string | null,
    previous: null as string | null,
  });

  useEffect(() => {
    fetchBooks();
    fetchCategories();
  }, [filters]);

  const fetchBooks = async () => {
    try {
      setIsLoading(true);
      const response = await bookService.getBooks(filters);
      setBooks(response.results);
      setPagination({
        count: response.count,
        next: response.next,
        previous: response.previous,
      });
    } catch (error) {
      toast.error('Failed to fetch books');
    } finally {
      setIsLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const cats = await bookService.getCategories();
      setCategories(cats);
    } catch (error) {
      console.error('Failed to fetch categories');
    }
  };

  const handleBorrow = async (book: Book) => {
    if (!isAuthenticated) {
      toast.error('Please login to borrow books');
      return;
    }

    setBorrowingId(book.id);
    try {
      await loanService.borrowBook(book.id);
      toast.success(`Successfully borrowed "${book.title}"`);
      fetchBooks();
    } catch (error: any) {
      toast.error(error.response?.data?.error || 'Failed to borrow book');
    } finally {
      setBorrowingId(null);
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setFilters({ ...filters, page: 1 });
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">Browse Books</h1>
        <p className="text-lg text-gray-600">Discover your next favorite read</p>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <form onSubmit={handleSearch} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="md:col-span-2">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                <input
                  type="text"
                  placeholder="Search by title, author, or ISBN..."
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  value={filters.search}
                  onChange={(e) => setFilters({ ...filters, search: e.target.value })}
                />
              </div>
            </div>

            <select
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              value={filters.category}
              onChange={(e) => setFilters({ ...filters, category: e.target.value, page: 1 })}
            >
              <option value="">All Categories</option>
              {categories.map((cat) => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
            </select>

            <select
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              value={filters.available === undefined ? '' : filters.available.toString()}
              onChange={(e) => setFilters({
                ...filters,
                available: e.target.value === '' ? undefined : e.target.value === 'true',
                page: 1,
              })}
            >
              <option value="">All Books</option>
              <option value="true">Available Only</option>
              <option value="false">Unavailable</option>
            </select>
          </div>

          <div className="flex justify-between items-center">
            <p className="text-sm text-gray-600">
              Showing {books.length} of {pagination.count} books
            </p>
            <Button type="submit" size="sm">
              Apply Filters
            </Button>
          </div>
        </form>
      </div>

      {/* Books Grid */}
      {isLoading ? (
        <div className="flex justify-center py-12">
          <LoadingSpinner size="lg" />
        </div>
      ) : books.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-xl text-gray-600">No books found</p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-8">
            {books.map((book) => (
              <BookCard
                key={book.id}
                book={book}
                onBorrow={handleBorrow}
                onView={(book) => {
                  setSelectedBook(book);
                  setShowDetails(true);
                }}
                isLoading={borrowingId === book.id}
              />
            ))}
          </div>

          {/* Pagination */}
          <div className="flex justify-center space-x-4">
            <Button
              variant="secondary"
              disabled={!pagination.previous}
              onClick={() => setFilters({ ...filters, page: (filters.page || 1) - 1 })}
            >
              Previous
            </Button>
            <span className="flex items-center px-4">
              Page {filters.page} of {Math.ceil(pagination.count / (filters.page_size || 12))}
            </span>
            <Button
              variant="secondary"
              disabled={!pagination.next}
              onClick={() => setFilters({ ...filters, page: (filters.page || 1) + 1 })}
            >
              Next
            </Button>
          </div>
        </>
      )}

      {/* Book Details Modal */}
      {selectedBook && (
        <Modal
          isOpen={showDetails}
          onClose={() => setShowDetails(false)}
          title="Book Details"
          size="lg"
        >
          <div className="space-y-4">
            <div>
              <h3 className="text-2xl font-bold text-gray-900">{selectedBook.title}</h3>
              <p className="text-lg text-gray-600 mt-1">by {selectedBook.author}</p>
            </div>

            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="font-semibold">ISBN:</span> {selectedBook.isbn}
              </div>
              <div>
                <span className="font-semibold">Category:</span> {selectedBook.category}
              </div>
              <div>
                <span className="font-semibold">Language:</span> {selectedBook.language}
              </div>
              <div>
                <span className="font-semibold">Pages:</span> {selectedBook.page_count}
              </div>
              {selectedBook.publisher && (
                <div>
                  <span className="font-semibold">Publisher:</span> {selectedBook.publisher}
                </div>
              )}
              {selectedBook.publication_date && (
                <div>
                  <span className="font-semibold">Published:</span> {formatDate(selectedBook.publication_date)}
                </div>
              )}
              <div>
                <span className="font-semibold">Available:</span> {selectedBook.available_copies}/{selectedBook.total_copies}
              </div>
            </div>

            {selectedBook.description && (
              <div>
                <h4 className="font-semibold mb-2">Description</h4>
                <p className="text-gray-700">{selectedBook.description}</p>
              </div>
            )}

            {isAuthenticated && selectedBook.is_available && (
              <Button
                className="w-full"
                onClick={() => {
                  handleBorrow(selectedBook);
                  setShowDetails(false);
                }}
                isLoading={borrowingId === selectedBook.id}
              >
                Borrow This Book
              </Button>
            )}
          </div>
        </Modal>
      )}
    </div>
  );
}
