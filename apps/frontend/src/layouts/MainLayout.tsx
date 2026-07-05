import { ReactNode, useEffect, useMemo, useState } from 'react';
import { NavLink, useLocation, useNavigate } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../state/hooks';
import { signOut } from '../state/slices/authSlice';
import { getDashboardMetrics } from '../services/api/dashboard';
import type { DashboardMetrics } from '../types';

interface MainLayoutProps {
  children: ReactNode;
}

export default function MainLayout({ children }: MainLayoutProps) {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const role = useAppSelector((state) => state.auth.role);
  const fullName = useAppSelector((state) => state.auth.fullName);
  const location = useLocation();
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [metricsLoading, setMetricsLoading] = useState(true);
  
  useEffect(() => {
    getDashboardMetrics()
      .then(setMetrics)
      .catch(() => setMetrics(null))
      .finally(() => setMetricsLoading(false));
  }, []);

  const pageTitle = useMemo(() => {
    if (location.pathname === '/dashboard') return 'Dashboard';
    if (location.pathname === '/tasks') return 'Tasks';
    if (location.pathname === '/tasks/create') return 'Create Task';
    if (location.pathname.startsWith('/tasks/') && location.pathname.endsWith('/edit')) return 'Edit Task';
    if (location.pathname.startsWith('/tasks/')) return 'Task Details';
    if (location.pathname === '/reports') return 'Reports';
    if (location.pathname === '/teams') return 'Teams';
    if (location.pathname === '/profile') return 'Profile';
    if (location.pathname === '/settings') return 'Settings';
    return 'Dashboard';
  }, [location.pathname]);

  const initials = fullName
    ? fullName
        .split(' ')
        .filter(Boolean)
        .slice(0, 2)
        .map((part) => part[0].toUpperCase())
        .join('')
    : 'TF';

  const designationMap = {
    ADMIN: 'Administrator',
    TEAM_LEAD: 'Team Lead',
    TEAM_MEMBER: 'Team Member',
  } as const;
  const designation = designationMap[role ?? 'TEAM_MEMBER'];

  const navItems = [
    { to: '/dashboard', label: 'Dashboard' },
    { to: '/tasks', label: 'Tasks' },
    ...(role === 'ADMIN' || role === 'TEAM_LEAD' ? [{ to: '/reports', label: 'Reports' }] : []),
    ...(role === 'ADMIN' || role === 'TEAM_LEAD' ? [{ to: '/teams', label: 'Teams' }] : []),
    { to: '/profile', label: 'Profile' },
    { to: '/settings', label: 'Settings' }
  ];

  const handleLogout = () => {
    window.localStorage.removeItem('authToken');
    window.localStorage.removeItem('authUserId');
    window.localStorage.removeItem('authFullName');
    window.localStorage.removeItem('authRole');
    dispatch(signOut());
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="sticky top-0 z-40 border-b border-slate-200 bg-slate-50/95 backdrop-blur backdrop-saturate-150">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
          <div
            role="button"
            tabIndex={0}
            onClick={() => navigate('/dashboard')}
            onKeyDown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') navigate('/dashboard');
            }}
            className="inline-flex items-center gap-3 cursor-pointer"
            title="Go to dashboard"
          >
            <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-sky-600 text-white">TF</div>
            <div>
              <p className="text-sm font-semibold text-slate-900">TaskFlow</p>
              <p className="text-xs text-slate-500">Productive task management</p>
            </div>
          </div>
          <div className="relative">
            <button
              type="button"
              onClick={() => setUserMenuOpen((open) => !open)}
              className="inline-flex items-center gap-3 rounded-full border border-slate-200 bg-white px-4 py-2 shadow-sm hover:bg-slate-50"
            >
              <span className="inline-flex h-10 w-10 items-center justify-center rounded-full bg-sky-600 text-sm font-semibold text-white">
                {initials}
              </span>
              <div className="text-left">
                <p className="text-sm font-semibold text-slate-900">{fullName ?? 'User'}</p>
                <p className="text-xs text-slate-500">{designation}</p>
              </div>
            </button>
            {userMenuOpen ? (
              <div className="absolute right-0 top-full mt-3 w-56 overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-lg">
                <button
                  type="button"
                  onClick={() => {
                    setUserMenuOpen(false);
                    navigate('/profile');
                  }}
                  className="w-full px-4 py-3 text-left text-sm text-slate-700 hover:bg-slate-50"
                >
                  Open Profile
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setUserMenuOpen(false);
                    navigate('/settings');
                  }}
                  className="w-full px-4 py-3 text-left text-sm text-slate-700 hover:bg-slate-50"
                >
                  Account Settings
                </button>
                <div className="border-t border-slate-200" />
                <button
                  type="button"
                  onClick={() => {
                    setUserMenuOpen(false);
                    handleLogout();
                  }}
                  className="w-full px-4 py-3 text-left text-sm font-semibold text-slate-900 hover:bg-slate-50"
                >
                  Sign Out
                </button>
              </div>
            ) : null}
          </div>
        </div>
      </div>
      <div className="mx-auto grid max-w-7xl gap-6 px-4 py-6 sm:px-6 lg:grid-cols-[260px_1fr]">
        <aside className="flex flex-col gap-6 rounded-[2rem] border border-slate-200 bg-white p-6 shadow-card">
          <div className="space-y-3">
            <div className="inline-flex items-center gap-3 rounded-3xl bg-slate-50 px-4 py-3">
              <div>
                <p className="text-xs uppercase tracking-[0.3em] text-slate-500">Current page</p>
                <p className="text-sm font-semibold text-slate-900">{pageTitle}</p>
              </div>
            </div>
            <nav className="space-y-2">
              {navItems.map((item) => (
                <NavLink
                  key={item.to}
                  to={item.to}
                  className={({ isActive }) =>
                    `block rounded-2xl px-4 py-3 text-sm font-medium transition ${
                      isActive
                        ? 'bg-sky-600 text-white shadow-sm'
                        : 'text-slate-600 hover:bg-slate-100'
                    }`
                  }
                >
                  {item.label}
                </NavLink>
              ))}
            </nav>
          </div>

          <div className="rounded-[1.75rem] border border-slate-200 bg-slate-50 p-5">
            <p className="text-xs font-semibold uppercase tracking-[0.24em] text-slate-400">Sprint Health</p>
            <div className="mt-4 grid gap-3">
              <div className="rounded-2xl bg-white p-4 shadow-sm">
                <p className="text-2xl font-semibold text-slate-900">
                  {metricsLoading ? '...' : `${metrics?.completionRate ?? 0}%`}
                </p>
                <p className="text-xs text-slate-500">
                  {metricsLoading
                    ? 'Loading...'
                    : metrics
                    ? metrics.completionRate >= 80
                      ? 'On track'
                      : metrics.completionRate >= 50
                      ? 'At risk'
                      : 'Off track'
                    : 'Unavailable'}
                </p>
              </div>
              <div className="rounded-2xl bg-white p-4 shadow-sm">
                <p className="text-2xl font-semibold text-slate-900">
                  {metricsLoading ? '...' : metrics?.dueTodayTasks ?? 0}
                </p>
                <p className="text-xs text-slate-500">Due today</p>
              </div>
            </div>
          </div>

          <button
            type="button"
            onClick={() => navigate('/tasks/create')}
            className="rounded-2xl bg-sky-600 px-4 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-sky-700"
          >
            + New Task
          </button>

          <button
            type="button"
            onClick={handleLogout}
            className="rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm font-semibold text-slate-700 transition hover:bg-slate-50"
          >
            Sign Out
          </button>
        </aside>

        <main className="space-y-6">{children}</main>
      </div>
    </div>
  );
}
