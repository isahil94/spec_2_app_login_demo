import { FormEvent, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../state/auth';
import './AuthPage.css';

export function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const from = (location.state as { from?: Location })?.from?.pathname || '/';
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    setLoading(true);
    const form = event.currentTarget;
    const email = (form.elements.namedItem('email') as HTMLInputElement).value;
    const password = (form.elements.namedItem('password') as HTMLInputElement).value;
    try {
      await login(email, password);
      navigate(from, { replace: true });
    } catch (err: any) {
      setError(err?.message || 'Sign in failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="auth-page" aria-labelledby="login-heading">
      <section className="auth-panel">
        <h1 id="login-heading">Sign In</h1>
        <form className="auth-form" onSubmit={handleSubmit}>
          <label htmlFor="email">Email</label>
          <input id="email" name="email" type="email" required placeholder="Enter your email" />

          <label htmlFor="password">Password</label>
          <input id="password" name="password" type="password" required placeholder="Enter your password" />

          <button type="submit" className="button primary" disabled={loading}>{loading ? 'Signing in…' : 'Sign In'}</button>
          <div className="auth-actions">
            <a className="forgot-link" href="/forgot-password">Forgot Password</a>
          </div>
          {error && <p className="auth-error" role="alert">{error}</p>}
          <p className="auth-footer">
            New here? <Link to="/register">Create an account</Link>
          </p>
        </form>
      </section>
    </main>
  );
}
