import { ReactNode, useEffect, useMemo, useState } from 'react';
import { NavLink, useLocation, useNavigate } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../state/hooks';
import { signOut } from '../state/slices/authSlice';
import { getDashboardMetrics } from '../services/api/dashboard';
import type { DashboardMetrics } from '../types';

interface MainLayoutProps {
  children: ReactNode;
}

interface NavItem {
  to: string;
  label: string;
  icon?: ReactNode;
}

const dashboardIcon = (
  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="h-3.5 w-3.5">
    <path d="M3 12L12 3L21 12V20C21 20.5523 20.5523 21 20 21H4C3.44772 21 3 20.5523 3 20V12Z" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
    <path d="M9 21V12H15V21" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

const taskListIcon = (
  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="h-3.5 w-3.5">
    <path d="M4 7H20" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
    <path d="M4 12H20" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
    <path d="M4 17H14" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
  </svg>
);

const profileIcon = (
  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="h-3.5 w-3.5">
    <path d="M12 12.75C14.0711 12.75 15.75 11.0711 15.75 9C15.75 6.92893 14.0711 5.25 12 5.25C9.92893 5.25 8.25 6.92893 8.25 9C8.25 11.0711 9.92893 12.75 12 12.75Z" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
    <path d="M4.5 20.25C4.5 16.9165 7.4165 14 10.75 14H13.25C16.5835 14 19.5 16.9165 19.5 20.25" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

const settingsIcon = (
  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="h-3.5 w-3.5">
    <path d="M12 15.5C13.933 15.5 15.5 13.933 15.5 12C15.5 10.067 13.933 8.5 12 8.5C10.067 8.5 8.5 10.067 8.5 12C8.5 13.933 10.067 15.5 12 15.5Z" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
    <path d="M19.4 15C19.3663 14.34 19.1667 13.7033 18.825 13.15L20.5 10.5L17.5 7.5L14.85 9.175C14.2967 8.83333 13.66 8.63367 13 8.6V5.5H11V8.6C10.34 8.63367 9.70333 8.83333 9.15 9.175L6.5 7.5L3.5 10.5L5.175 13.15C4.83333 13.7033 4.63367 14.34 4.6 15H1.5V17H4.6C4.63367 17.66 4.83333 18.2967 5.175 18.85L3.5 21.5L6.5 24.5L9.15 22.825C9.70333 23.1667 10.34 23.3663 11 23.4V26.5H13V23.4C13.66 23.3663 14.2967 23.1667 14.85 22.825L17.5 24.5L20.5 21.5L18.825 18.85C19.1667 18.2967 19.3663 17.66 19.4 17H22.5V15H19.4Z" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

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

  const navItems: NavItem[] = [
    { to: '/dashboard', label: 'Dashboard', icon: dashboardIcon },
    { to: '/tasks', label: 'Task List', icon: taskListIcon },
    { to: '/profile', label: 'Profile', icon: profileIcon },
    { to: '/settings', label: 'Settings', icon: settingsIcon }
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
              <p className="text-sm font-semibold brand-text">TaskFlow</p>
              <p className="text-xs brand-subtext">Productive task management</p>
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
                    `flex items-center gap-3 rounded-2xl px-4 py-3 text-sm font-medium transition ${
                      isActive
                        ? 'bg-sky-600 text-white shadow-sm'
                        : 'text-slate-600 hover:bg-slate-100'
                    }`
                  }
                >
                  {item.icon ? (
                    <span className="inline-flex h-9 w-9 items-center justify-center rounded-2xl bg-slate-100 text-slate-700 transition hover:bg-slate-200">
                      {item.icon}
                    </span>
                  ) : null}
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
