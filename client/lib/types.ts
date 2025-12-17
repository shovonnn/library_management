export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  phone_number?: string;
  address?: string;
  role: 'admin' | 'user';
  date_joined: string;
}

export interface Book {
  id: number;
  title: string;
  author: string;
  isbn: string;
  publisher?: string;
  publication_date?: string;
  page_count: number;
  language: string;
  description?: string;
  category: string;
  total_copies: number;
  available_copies: number;
  cover_image?: string;
  is_available: boolean;
  created_at: string;
  updated_at: string;
}

export interface Loan {
  id: number;
  user: User;
  book: Book;
  borrow_date: string;
  due_date: string;
  return_date?: string;
  status: 'borrowed' | 'returned' | 'overdue';
  is_overdue: boolean;
  days_overdue: number;
  fine_amount: string;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  password2: string;
  first_name: string;
  last_name: string;
  phone_number?: string;
  address?: string;
}

export interface AuthResponse {
  access: string;
  refresh: string;
}

export interface BookFilters {
  search?: string;
  category?: string;
  author?: string;
  available?: boolean;
  page?: number;
  page_size?: number;
}
