import api, { setAuthTokens, clearAuthTokens } from './api';
import { User, LoginCredentials, RegisterData, AuthResponse } from './types';

export const authService = {
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await api.post<AuthResponse>('/auth/login/', credentials);
    setAuthTokens(response.data.access, response.data.refresh);
    return response.data;
  },

  async register(data: RegisterData): Promise<{ user: User; message: string }> {
    const response = await api.post('/auth/register/', data);
    return response.data;
  },

  async getProfile(): Promise<User> {
    const response = await api.get<User>('/auth/profile/');
    return response.data;
  },

  async updateProfile(data: Partial<User>): Promise<User> {
    const response = await api.patch<User>('/auth/profile/', data);
    return response.data;
  },

  async changePassword(oldPassword: string, newPassword: string): Promise<void> {
    await api.post('/auth/change-password/', {
      old_password: oldPassword,
      new_password: newPassword,
      new_password2: newPassword,
    });
  },

  logout(): void {
    clearAuthTokens();
  },
};
