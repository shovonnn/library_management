import api from './api';
import { Loan, PaginatedResponse } from './types';

export const loanService = {
  async borrowBook(bookId: number): Promise<Loan> {
    const response = await api.post<Loan>('/loans/', { book_id: bookId });
    return response.data;
  },

  async returnBook(loanId: number): Promise<Loan> {
    const response = await api.post<Loan>(`/loans/${loanId}/return/`);
    return response.data;
  },

  async getMyLoans(status?: string): Promise<PaginatedResponse<Loan>> {
    const params = status ? `?status=${status}` : '';
    const response = await api.get<PaginatedResponse<Loan>>(`/loans/my-loans/${params}`);
    return response.data;
  },

  async getAllLoans(page?: number): Promise<PaginatedResponse<Loan>> {
    const params = page ? `?page=${page}` : '';
    const response = await api.get<PaginatedResponse<Loan>>(`/loans/${params}`);
    return response.data;
  },

  async getLoan(id: number): Promise<Loan> {
    const response = await api.get<Loan>(`/loans/${id}/`);
    return response.data;
  },
};
