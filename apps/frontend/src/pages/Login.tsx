import { FormEvent, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAppDispatch } from '../state/hooks';
import { signInSuccess, setAuthError } from '../state/slices/authSlice';
import { signIn } from '../services/api/auth';
import Button from '../components/Button';
import FormField from '../components/FormField';
import Tooltip from '../components/Tooltip';
import { useEffect } from 'react';

export default function LoginPage() {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [fieldErrors, setFieldErrors] = useState<{ email?: string; password?: string }>({});
  const [submitting, setSubmitting] = useState(false);

  const validateEmail = () => {
    const emailRegex = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
    if (!email.trim() || !emailRegex.test(email)) {
      setFieldErrors((s) => ({ ...s, email: 'Please enter a valid email address.' }));
      return false;
    }
    setFieldErrors((s) => ({ ...s, email: undefined }));
    return true;
  };

  const validatePassword = () => {
    if (!password.trim()) {
      setFieldErrors((s) => ({ ...s, password: 'Password is required.' }));
      return false;
    }
    setFieldErrors((s) => ({ ...s, password: undefined }));
    return true;
  };

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setError(null);
    if (!validateEmail() || !validatePassword()) {
      return;
    }
    setSubmitting(true);
    try {
      const data = await signIn({ email, password });
      window.localStorage.setItem('authToken', data.token);
      window.localStorage.setItem('authUserId', data.user.userId);
      window.localStorage.setItem('authFullName', data.user.fullName ?? '');
      window.localStorage.setItem('authRole', data.user.role);
      dispatch(signInSuccess({ token: data.token, userId: data.user.userId, fullName: data.user.fullName, role: data.user.role }));
      navigate('/dashboard');
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Sign in failed. Please try again.';
      setError(message);
      dispatch(setAuthError(message));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-4xl font-semibold text-slate-900">Welcome back</h1>
        <p className="mt-2 text-sm text-slate-600">Sign in to continue to your task workspace.</p>
      </div>
      <form className="space-y-5" onSubmit={handleSubmit} noValidate>
        <FormField label="Email Address">
          <div className="relative">
            <input
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(event) => {
                setEmail(event.target.value);
                setFieldErrors((s) => ({ ...s, email: undefined }));
                setError(null);
              }}
              onBlur={validateEmail}
              className="w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
              required
            />
            {fieldErrors.email ? <Tooltip message={fieldErrors.email} /> : null}
          </div>
        </FormField>
        <FormField label="Password">
          <div className="relative">
            <input
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(event) => {
                setPassword(event.target.value);
                setFieldErrors((s) => ({ ...s, password: undefined }));
                setError(null);
              }}
              onBlur={validatePassword}
              className="w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
              required
              minLength={8}
            />
            {fieldErrors.password ? <Tooltip message={fieldErrors.password} /> : null}
          </div>
        </FormField>
        {error ? <p className="text-sm text-rose-600">{error}</p> : null}
        <div className="space-y-4">
          <Button type="submit" disabled={submitting} className="w-full">
            {submitting ? 'Signing in...' : 'Sign In'}
          </Button>
          <div className="flex items-center justify-between text-sm text-slate-600">
            <Link to="/forgot-password" className="text-blue-600 hover:underline">
              Forgot password?
            </Link>
            <Link to="/register" className="font-medium text-slate-900 hover:text-slate-700">
              Create account
            </Link>
          </div>
        </div>
      </form>
    </div>
  );
}
