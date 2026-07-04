import { apiClient } from './client';

export interface LoginRequest {
  email: string;
  password: string;
  rememberMe?: boolean;
}

export interface RegisterRequest {
  email: string;
  password: string;
  fullName: string;
}

export interface AuthUser {
  userId: string;
  email: string;
  fullName?: string | null;
  role: 'ADMIN' | 'TEAM_LEAD' | 'TEAM_MEMBER';
}

export interface LoginResponse {
  data: {
    token: string;
    expiresIn: number;
    user: AuthUser;
  };
}

export interface RegisterResponse {
  data: {
    userId: string;
    email: string;
    fullName: string;
    role: 'TEAM_MEMBER';
    createdAt: string;
  };
}

export const signIn = async (payload: LoginRequest) => {
  const response = await apiClient.post<LoginResponse>('/auth/login', payload);
  return response.data.data;
};

export const register = async (payload: RegisterRequest) => {
  const response = await apiClient.post<RegisterResponse>('/auth/register', payload);
  return response.data.data;
};
