'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/store';
import { Book } from '@/lib/types';
import { bookService } from '@/lib/book.service';
import { loanService } from '@/lib/loan.service';
import { Card, CardBody, CardHeader } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Modal } from '@/components/ui/Modal';
import { LoadingPage, LoadingSpinner } from '@/components/ui/Loading';
import { BookOpen, Users, TrendingUp, Plus, Edit, Trash2 } from 'lucide-react';
import toast from 'react-hot-toast';
import { useForm } from 'react-hook-form';

export default function AdminPage() {
  const router = useRouter();
  const { user, isAuthenticated, isLoading: authLoading } = useAuthStore();
  const [books, setBooks] = useState<Book[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [selectedBook, setSelectedBook] = useState<Book | null>(null);
  const [isSaving, setIsSaving] = useState(false);
  const [stats, setStats] = useState({
    totalBooks: 0,
    totalLoans: 0,
    activeLoans: 0,
  });

  const { register, handleSubmit, formState: { errors }, reset } = useForm<Partial<Book>>();

  useEffect(() => {
    if (!authLoading) {
      if (!isAuthenticated || user?.role !== 'admin') {
        router.push('/');
        toast.error('Access denied. Admin only.');
        return;
      }
      fetchBooks();
      fetchStats();
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isAuthenticated, user, authLoading]);

  const fetchBooks = async () => {
    try {
      setIsLoading(true);
      const response = await bookService.getBooks({ page_size: 100 });
      setBooks(response.results);
    } catch (error) {
      toast.error('Failed to fetch books');
    } finally {
      setIsLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const [booksRes, loansRes] = await Promise.all([
        bookService.getBooks({ page_size: 1 }),
        loanService.getAllLoans(),
      ]);
      setStats({
        totalBooks: booksRes.count,
        totalLoans: loansRes.count,
        activeLoans: loansRes.results.filter(l => l.status === 'borrowed').length,
      });
    } catch (error) {
      console.error('Failed to fetch stats');
    }
  };

  const handleAddBook = async (data: Partial<Book>) => {
    setIsSaving(true);
    try {
      await bookService.createBook(data);
      toast.success('Book added successfully');
      setShowAddModal(false);
      reset();
      fetchBooks();
      fetchStats();
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to add book');
    } finally {
      setIsSaving(false);
    }
  };

  const handleEditBook = async (data: Partial<Book>) => {
    if (!selectedBook) return;
    setIsSaving(true);
    try {
      await bookService.updateBook(selectedBook.id, data);
      toast.success('Book updated successfully');
      setShowEditModal(false);
      setSelectedBook(null);
      fetchBooks();
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to update book');
    } finally {
      setIsSaving(false);
    }
  };

  const handleDeleteBook = async (bookId: number) => {
    if (!confirm('Are you sure you want to delete this book?')) return;
    
    try {
      await bookService.deleteBook(bookId);
      toast.success('Book deleted successfully');
      fetchBooks();
      fetchStats();
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to delete book');
    }
  };

  const openEditModal = (book: Book) => {
    setSelectedBook(book);
    reset(book);
    setShowEditModal(true);
  };

  if (authLoading || isLoading) {
    return <LoadingPage />;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">Admin Dashboard</h1>
        <p className="text-lg text-gray-600">Manage books and monitor library statistics</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <Card>
          <CardBody className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Total Books</p>
                <p className="text-3xl font-bold text-gray-900">{stats.totalBooks}</p>
              </div>
              <div className="bg-primary-100 rounded-full p-3">
                <BookOpen className="h-8 w-8 text-primary-600" />
              </div>
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Active Loans</p>
                <p className="text-3xl font-bold text-gray-900">{stats.activeLoans}</p>
              </div>
              <div className="bg-green-100 rounded-full p-3">
                <TrendingUp className="h-8 w-8 text-green-600" />
              </div>
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Total Loans</p>
                <p className="text-3xl font-bold text-gray-900">{stats.totalLoans}</p>
              </div>
              <div className="bg-purple-100 rounded-full p-3">
                <Users className="h-8 w-8 text-purple-600" />
              </div>
            </div>
          </CardBody>
        </Card>
      </div>

      {/* Books Management */}
      <Card>
        <CardHeader>
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-semibold">Books Management</h2>
            <Button onClick={() => setShowAddModal(true)}>
              <Plus className="h-4 w-4 mr-2" />
              Add Book
            </Button>
          </div>
        </CardHeader>
        <CardBody>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Title</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Author</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Category</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Available</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {books.map((book) => (
                  <tr key={book.id} className="hover:bg-gray-50">
                    <td className="px-4 py-4 text-sm font-medium text-gray-900">{book.title}</td>
                    <td className="px-4 py-4 text-sm text-gray-600">{book.author}</td>
                    <td className="px-4 py-4 text-sm text-gray-600">{book.category}</td>
                    <td className="px-4 py-4 text-sm text-gray-600">
                      {book.available_copies}/{book.total_copies}
                    </td>
                    <td className="px-4 py-4 text-sm">
                      <div className="flex space-x-2">
                        <button
                          onClick={() => openEditModal(book)}
                          className="text-primary-600 hover:text-primary-800"
                        >
                          <Edit className="h-4 w-4" />
                        </button>
                        <button
                          onClick={() => handleDeleteBook(book.id)}
                          className="text-red-600 hover:text-red-800"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardBody>
      </Card>

      {/* Add Book Modal */}
      <Modal
        isOpen={showAddModal}
        onClose={() => setShowAddModal(false)}
        title="Add New Book"
        size="lg"
      >
        <form onSubmit={handleSubmit(handleAddBook)} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="Title"
              error={errors.title?.message}
              {...register('title', { required: 'Title is required' })}
            />
            <Input
              label="Author"
              error={errors.author?.message}
              {...register('author', { required: 'Author is required' })}
            />
            <Input
              label="ISBN"
              error={errors.isbn?.message}
              {...register('isbn', { required: 'ISBN is required' })}
            />
            <Input
              label="Category"
              error={errors.category?.message}
              {...register('category', { required: 'Category is required' })}
            />
            <Input
              label="Publisher"
              {...register('publisher')}
            />
            <Input
              label="Publication Date"
              type="date"
              {...register('publication_date')}
            />
            <Input
              label="Page Count"
              type="number"
              error={errors.page_count?.message}
              {...register('page_count', { required: 'Page count is required', min: 1 })}
            />
            <Input
              label="Language"
              {...register('language')}
            />
            <Input
              label="Total Copies"
              type="number"
              error={errors.total_copies?.message}
              {...register('total_copies', { required: 'Total copies is required', min: 1 })}
            />
            <Input
              label="Available Copies"
              type="number"
              error={errors.available_copies?.message}
              {...register('available_copies', { required: 'Available copies is required', min: 0 })}
            />
          </div>
          <Input
            label="Description"
            {...register('description')}
          />
          <Input
            label="Cover Image URL"
            {...register('cover_image')}
          />
          <Button type="submit" className="w-full" isLoading={isSaving}>
            Add Book
          </Button>
        </form>
      </Modal>

      {/* Edit Book Modal */}
      <Modal
        isOpen={showEditModal}
        onClose={() => setShowEditModal(false)}
        title="Edit Book"
        size="lg"
      >
        <form onSubmit={handleSubmit(handleEditBook)} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="Title"
              error={errors.title?.message}
              {...register('title', { required: 'Title is required' })}
            />
            <Input
              label="Author"
              error={errors.author?.message}
              {...register('author', { required: 'Author is required' })}
            />
            <Input
              label="ISBN"
              error={errors.isbn?.message}
              {...register('isbn', { required: 'ISBN is required' })}
            />
            <Input
              label="Category"
              error={errors.category?.message}
              {...register('category', { required: 'Category is required' })}
            />
            <Input
              label="Publisher"
              {...register('publisher')}
            />
            <Input
              label="Publication Date"
              type="date"
              {...register('publication_date')}
            />
            <Input
              label="Page Count"
              type="number"
              error={errors.page_count?.message}
              {...register('page_count', { required: 'Page count is required', min: 1 })}
            />
            <Input
              label="Language"
              {...register('language')}
            />
            <Input
              label="Total Copies"
              type="number"
              error={errors.total_copies?.message}
              {...register('total_copies', { required: 'Total copies is required', min: 1 })}
            />
            <Input
              label="Available Copies"
              type="number"
              error={errors.available_copies?.message}
              {...register('available_copies', { required: 'Available copies is required', min: 0 })}
            />
          </div>
          <Input
            label="Description"
            {...register('description')}
          />
          <Input
            label="Cover Image URL"
            {...register('cover_image')}
          />
          <Button type="submit" className="w-full" isLoading={isSaving}>
            Update Book
          </Button>
        </form>
      </Modal>
    </div>
  );
}
