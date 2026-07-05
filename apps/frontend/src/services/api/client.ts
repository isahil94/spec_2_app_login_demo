import axios, { AxiosError } from 'axios';
import { store } from '../../state/store';
import { signOut } from '../../state/slices/authSlice';

const API_BASE_URL = 'http://localhost:8001/api/v1';

const clearAuthSession = () => {
  if (typeof window !== 'undefined') {
    window.localStorage.removeItem('authToken');
    window.localStorage.removeItem('authUserId');
    window.localStorage.removeItem('authFullName');
    window.localStorage.removeItem('authRole');
  }
  store.dispatch(signOut());
};

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 12000
});

apiClient.interceptors.request.use((config) => {
  const token = typeof window !== 'undefined' ? window.localStorage.getItem('authToken') : null;
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Error response interceptor to extract meaningful error messages
const API_ORIGIN = new URL(API_BASE_URL).origin;

apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError<any>) => {
    if (error.response?.status === 401 || error.response?.status === 403) {
      clearAuthSession();
      if (typeof window !== 'undefined' && window.location.pathname !== '/login') {
        window.location.assign('/login');
      }
    }

    let errorMessage = 'An error occurred. Please try again.';

    // If server returned a JSON error body, prefer that message
    if (error.response?.data) {
      const data = error.response.data;
      if (data.error?.message) {
        errorMessage = data.error.message;
      } else if (Array.isArray(data.detail)) {
        errorMessage = data.detail.map((d: any) => d.msg || JSON.stringify(d)).join('; ');
      } else if (typeof data.detail === 'string') {
        errorMessage = data.detail;
      }
    }

    // No response from server -> network / backend unreachable
    else if (!error.response) {
      if (typeof window !== 'undefined') {
        // Offline detection
        if (!window.navigator.onLine) {
          errorMessage = 'No internet connection. Please check your network and try again.';
        } else {
          // Try a quick health-check to determine if backend is up
          const healthUrl = `${API_ORIGIN}/health`;
          try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 3000);
            const resp = await fetch(healthUrl, { cache: 'no-cache', signal: controller.signal });
            clearTimeout(timeoutId);
            if (resp.ok) {
              errorMessage = 'Request failed — server did not respond. Try again.';
            } else {
              errorMessage = 'Backend server is unreachable. It may be down or restarting.';
            }
          } catch (e) {
            errorMessage = 'Cannot reach backend server. It may be down or refusing connections.';
          }
        }
      } else {
        errorMessage = 'Network error. Please check your connection.';
      }
    }

    // Fallback to axios message
    else if (error.message) {
      errorMessage = error.message;
    }

    if (axios.isAxiosError(error)) {
      error.message = errorMessage;
    }

    return Promise.reject(error);
  }
);

export function isDependencyUnavailable(error: unknown): boolean {
  if (!axios.isAxiosError(error)) {
    return false;
  }
  return error.response?.status === 503;
}
