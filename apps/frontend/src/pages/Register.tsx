import { FormEvent, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAppDispatch } from '../state/hooks';
import { register, signIn } from '../services/api/auth';
import { signInSuccess } from '../state/slices/authSlice';
import Button from '../components/Button';
import FormField from '../components/FormField';
import Tooltip from '../components/Tooltip';

export default function RegisterPage() {
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [fieldErrors, setFieldErrors] = useState<{
    fullName?: string;
    email?: string;
    password?: string;
    confirmPassword?: string;
  }>({});
  const [submitting, setSubmitting] = useState(false);
  const navigate = useNavigate();
  const dispatch = useAppDispatch();

  // Field validators (used on blur)
  const validateFullName = () => {
    if (!fullName.trim()) {
      setFieldErrors((s) => ({ ...s, fullName: 'Full name is required.' }));
      return false;
    }
    setFieldErrors((s) => ({ ...s, fullName: undefined }));
    return true;
  };

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
    if (password.length < 8) {
      setFieldErrors((s) => ({ ...s, password: 'Password must be at least 8 characters.' }));
      return false;
    }
    setFieldErrors((s) => ({ ...s, password: undefined }));
    return true;
  };

  const validateConfirmPassword = () => {
    if (confirmPassword !== password) {
      setFieldErrors((s) => ({ ...s, confirmPassword: 'Passwords do not match.' }));
      return false;
    }
    setFieldErrors((s) => ({ ...s, confirmPassword: undefined }));
    return true;
  };

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setError(null);
    setFieldErrors({});

    // Client-side validation
    const errors: {
      fullName?: string;
      email?: string;
      password?: string;
      confirmPassword?: string;
    } = {};
    if (!fullName.trim()) errors.fullName = 'Full name is required.';
    const emailRegex = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
    if (!email.trim() || !emailRegex.test(email)) errors.email = 'Please enter a valid email address.';
    if (password.length < 8) errors.password = 'Password must be at least 8 characters.';
    if (confirmPassword !== password) errors.confirmPassword = 'Passwords do not match.';

    if (Object.keys(errors).length > 0) {
      setFieldErrors(errors);
      return;
    }

    setSubmitting(true);
    try {
      await register({ fullName, email, password });
      const auth = await signIn({ email, password });
      window.localStorage.setItem('authToken', auth.token);
      window.localStorage.setItem('authUserId', auth.user.userId);
      window.localStorage.setItem('authFullName', auth.user.fullName ?? '');
      window.localStorage.setItem('authRole', auth.user.role);
      dispatch(signInSuccess({ token: auth.token, userId: auth.user.userId, fullName: auth.user.fullName, role: auth.user.role }));
      navigate('/dashboard');
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Registration failed. Please try again.';
      // show server error once in a prominent place
      setError(message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-4xl font-semibold text-slate-900">Create your account</h1>
        <p className="mt-2 text-sm text-slate-600">Start managing your tasks with your team today.</p>
      </div>
      <form className="space-y-5" onSubmit={handleSubmit} noValidate>
        {error ? <div className="rounded-2xl bg-rose-50 p-4 text-sm text-rose-700">{error}</div> : null}
        <FormField label="Full Name">
          <div className="relative">
            <input
              type="text"
              placeholder="Enter full name"
              value={fullName}
              onChange={(event) => {
                setFullName(event.target.value);
                setFieldErrors((s) => ({ ...s, fullName: undefined }));
                setError(null);
              }}
              onBlur={validateFullName}
              className="w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
              required
            />
            {fieldErrors.fullName ? <Tooltip message={fieldErrors.fullName} /> : null}
          </div>
        </FormField>
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
              placeholder="Create a password"
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
            <p className="mt-2 text-xs text-slate-500">Password must be at least 8 characters.</p>
          </div>
        </FormField>
        <FormField label="Confirm Password">
          <div className="relative">
            <input
              type="password"
              placeholder="Confirm your password"
              value={confirmPassword}
              onChange={(event) => {
                setConfirmPassword(event.target.value);
                setFieldErrors((s) => ({ ...s, confirmPassword: undefined }));
                setError(null);
              }}
              onBlur={validateConfirmPassword}
              className="w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
              required
            />
            {fieldErrors.confirmPassword ? <Tooltip message={fieldErrors.confirmPassword} /> : null}
          </div>
        </FormField>
        <div className="space-y-4">
          <Button type="submit" disabled={submitting} className="w-full">
            {submitting ? 'Creating account...' : 'Create Account'}
          </Button>
          <div className="text-sm text-slate-600">
            <span>Already have an account? </span>
            <Link to="/login" className="font-semibold text-slate-900 hover:text-slate-700">
              Sign in
            </Link>
          </div>
        </div>
      </form>
    </div>
  );
}
