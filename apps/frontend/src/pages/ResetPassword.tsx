import { FormEvent, useState } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import Button from '../components/Button';

export default function ResetPasswordPage() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');
  const [password, setPassword] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    if (!password || password.length < 8) {
      setError('Password must be at least 8 characters.');
      return;
    }
    if (!token) {
      setError('Reset token is missing.');
      return;
    }
    setSubmitted(true);
  };

  return (
    <div>
      <h1 className="mb-4 text-2xl font-semibold text-slate-900">Reset Password</h1>
      <p className="mb-6 text-sm text-slate-600">Enter a new password to restore access to your account.</p>
      {submitted ? (
        <div className="rounded-3xl border border-slate-200 bg-slate-50 p-6 text-slate-700 shadow-card">
          <p className="font-medium">Password reset successfully</p>
          <p className="mt-2 text-sm">You may now sign in with your new password.</p>
          <Link to="/login" className="mt-4 inline-block text-sm text-blue-600 hover:underline">
            Return to Login
          </Link>
        </div>
      ) : (
        <form className="space-y-5" onSubmit={handleSubmit} noValidate>
          <label className="block text-sm font-medium text-slate-700">
            New Password
            <input
              type="password"
              placeholder="Enter new password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              className="mt-2 w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
              required
              minLength={8}
            />
          </label>
          {error ? <p className="text-sm text-rose-600">{error}</p> : null}
          <Button type="submit">Reset Password</Button>
        </form>
      )}
    </div>
  );
}
