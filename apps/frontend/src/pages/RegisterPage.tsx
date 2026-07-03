import { Link, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { useAuth } from '../state/auth';
import './AuthPage.css';

export function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    setLoading(true);
    const form = event.currentTarget;
    const displayName = (form.elements.namedItem('displayName') as HTMLInputElement).value;
    const email = (form.elements.namedItem('email') as HTMLInputElement).value;
    const password = (form.elements.namedItem('password') as HTMLInputElement).value;
    const confirm = (form.elements.namedItem('confirm') as HTMLInputElement)?.value;

    if (password !== confirm) {
      setError('Passwords do not match');
      setLoading(false);
      return;
    }

    try {
      await register(displayName, email, password);
      navigate('/', { replace: true });
    } catch (err: any) {
      setError(err?.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="auth-page" aria-labelledby="register-heading">
      <section className="auth-panel">
        <h1 id="register-heading">Create your account</h1>
        <form className="auth-form" onSubmit={handleSubmit}>
          <label htmlFor="displayName">Full Name</label>
          <input id="displayName" name="displayName" type="text" required placeholder="Enter your full name" />

          <label htmlFor="email">Email</label>
          <input id="email" name="email" type="email" required placeholder="Enter your email" />

          <label htmlFor="password">Password</label>
          <input id="password" name="password" type="password" required placeholder="Enter your password" />

          <label htmlFor="confirm">Confirm password</label>
          <input id="confirm" name="confirm" type="password" required placeholder="Confirm your password" />

          <button type="submit" className="button primary" disabled={loading}>{loading ? 'Creating…' : 'Create Account'}</button>
          {error && <p className="auth-error" role="alert">{error}</p>}
          <p className="auth-footer">
            Already have an account? <Link to="/login">Sign in</Link>
          </p>
        </form>
      </section>
    </main>
  );
}
