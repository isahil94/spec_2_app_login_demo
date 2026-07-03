import { createContext, useContext, useEffect, useMemo, useState } from 'react';
import { authService } from '../services/api/authService';

interface User {
  email: string;
  displayName?: string;
}

interface StoredUser extends User {
  password: string;
}

interface AuthContextValue {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  register: (displayName: string, email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);
const STORAGE_KEY = 'taskflow-user';

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const token = authService.getToken();
    if (!token) return;
    let mounted = true;
    authService
      .me()
      .then((profile) => {
        if (!mounted) return;
        const newUser: User = { email: profile.email, displayName: profile.full_name };
        window.localStorage.setItem(STORAGE_KEY, JSON.stringify(newUser));
        setUser(newUser);
      })
      .catch(() => {
        authService.clearToken();
      });
    return () => {
      mounted = false;
    };
  }, []);

  const login = async (email: string, password: string) => {
    await authService.login(email, password);
    const profile = await authService.me();
    const newUser: User = { email: profile.email, displayName: profile.full_name };
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(newUser));
    setUser(newUser);
  };

  const logout = () => {
    window.localStorage.removeItem(STORAGE_KEY);
    setUser(null);
  };

  const register = async (displayName: string, email: string, password: string) => {
    await authService.register(displayName, email, password);
    const profile = await authService.me();
    const newUser: User = { email: profile.email, displayName: profile.full_name };
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(newUser));
    setUser(newUser);
  };

  const value = useMemo(() => ({ user, login, register, logout }), [user]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
