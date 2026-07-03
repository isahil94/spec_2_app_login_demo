const API_BASE = 'http://127.0.0.1:8001/api/v1';
const TOKEN_KEY = 'taskflow-token';

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

async function post(path: string, body: any) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || 'Request failed');
  }
  return res.json();
}

export async function register(full_name: string, email: string, password: string): Promise<TokenResponse> {
  const data = await post('/auth/register', { full_name, email, password });
  if (data?.access_token) {
    window.localStorage.setItem(TOKEN_KEY, data.access_token);
  }
  return data;
}

export async function login(email: string, password: string): Promise<TokenResponse> {
  const data = await post('/auth/login', { email, password });
  if (data?.access_token) {
    window.localStorage.setItem(TOKEN_KEY, data.access_token);
  }
  return data;
}

export function getToken(): string | null {
  return window.localStorage.getItem(TOKEN_KEY);
}

export function clearToken() {
  window.localStorage.removeItem(TOKEN_KEY);
}

export async function me() {
  const token = getToken();
  if (!token) throw new Error('No token');
  const res = await fetch(`${API_BASE}/auth/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || 'Unable to fetch profile');
  }
  return res.json();
}

export const authService = { register, login, me, getToken, clearToken };
