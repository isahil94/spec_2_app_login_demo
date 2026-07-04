import { FormEvent, useState } from 'react';
import { Link } from 'react-router-dom';
import Button from '../components/Button';

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    if (!email.trim()) {
      return;
    }
    setSubmitted(true);
  };

  return (
    <div>
      <h1 className="mb-4 text-2xl font-semibold text-slate-900">Forgot Password</h1>
      <p className="mb-6 text-sm text-slate-600">Enter your email to receive password recovery instructions.</p>
      {submitted ? (
        <div className="rounded-3xl border border-slate-200 bg-slate-50 p-6 text-slate-700 shadow-card">
          <p className="font-medium">Recovery email sent</p>
          <p className="mt-2 text-sm">If that email exists, you will receive instructions shortly.</p>
          <Link to="/login" className="mt-4 inline-block text-sm text-blue-600 hover:underline">
            Return to Login
          </Link>
        </div>
      ) : (
        <form className="space-y-5" onSubmit={handleSubmit}>
          <label className="block text-sm font-medium text-slate-700">
            Email Address
            <input
              type="email"
              placeholder="Enter email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              className="mt-2 w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
              required
            />
          </label>
          <div className="flex items-center justify-between gap-4">
            <Button type="submit">Send Recovery Email</Button>
            <Link to="/login" className="text-sm font-medium text-slate-700 hover:text-slate-900">
              Back to Login
            </Link>
          </div>
        </form>
      )}
    </div>
  );
}
