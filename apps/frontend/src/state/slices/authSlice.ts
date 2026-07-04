import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface AuthState {
  isAuthenticated: boolean;
  token: string | null;
  userId: string | null;
  fullName: string | null;
  role: 'ADMIN' | 'TEAM_LEAD' | 'TEAM_MEMBER' | null;
  error: string | null;
}

const persistedToken = typeof window !== 'undefined' ? window.localStorage.getItem('authToken') : null;
const persistedUserId = typeof window !== 'undefined' ? window.localStorage.getItem('authUserId') : null;
const persistedFullName = typeof window !== 'undefined' ? window.localStorage.getItem('authFullName') : null;
const persistedRole = typeof window !== 'undefined' ? (window.localStorage.getItem('authRole') as AuthState['role'] | null) : null;

const initialState: AuthState = {
  isAuthenticated: Boolean(persistedToken && persistedUserId && persistedRole),
  token: persistedToken,
  userId: persistedUserId,
  fullName: persistedFullName,
  role: persistedRole,
  error: null
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    signInSuccess(state, action: PayloadAction<{ token: string; userId: string; fullName?: string | null; role: AuthState['role'] }>) {
      state.isAuthenticated = true;
      state.token = action.payload.token;
      state.userId = action.payload.userId;
      state.fullName = action.payload.fullName ?? null;
      state.role = action.payload.role;
      state.error = null;
    },
    signOut(state) {
      state.isAuthenticated = false;
      state.token = null;
      state.userId = null;
      state.fullName = null;
      state.role = null;
      state.error = null;
    },
    setAuthError(state, action: PayloadAction<string | null>) {
      state.error = action.payload;
    }
  }
});

export const { signInSuccess, signOut, setAuthError } = authSlice.actions;
export default authSlice.reducer;
