import api from './api';
import { Book, PaginatedResponse, BookFilters } from './types';

export const bookService = {
  async getBooks(filters?: BookFilters): Promise<PaginatedResponse<Book>> {
    const params = new URLSearchParams();
    
    if (filters?.search) params.append('search', filters.search);
    if (filters?.category) params.append('category', filters.category);
    if (filters?.author) params.append('author', filters.author);
    if (filters?.available !== undefined) params.append('available', String(filters.available));
    if (filters?.page) params.append('page', String(filters.page));
    if (filters?.page_size) params.append('page_size', String(filters.page_size));

    const response = await api.get<PaginatedResponse<Book>>(`/books/?${params.toString()}`);
    return response.data;
  },

  async getBook(id: number): Promise<Book> {
    const response = await api.get<Book>(`/books/${id}/`);
    return response.data;
  },

  async createBook(data: Partial<Book>): Promise<Book> {
    const response = await api.post<Book>('/books/', data);
    return response.data;
  },

  async updateBook(id: number, data: Partial<Book>): Promise<Book> {
    const response = await api.patch<Book>(`/books/${id}/`, data);
    return response.data;
  },

  async deleteBook(id: number): Promise<void> {
    await api.delete(`/books/${id}/`);
  },

  async getCategories(): Promise<string[]> {
    const response = await api.get<string[]>('/books/categories/');
    return response.data;
  },
};
