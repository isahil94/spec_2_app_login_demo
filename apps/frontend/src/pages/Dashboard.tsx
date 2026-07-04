import { Link } from 'react-router-dom';
import { useEffect, useMemo, useState } from 'react';
import { getDashboardMetrics } from '../services/api/dashboard';
import type { DashboardMetrics } from '../types';

const formatDay = (isoDate: string) =>
  new Date(isoDate).toLocaleDateString(undefined, { weekday: 'short' });

function StatBar({ color, value }: { color: string; value: number }) {
  return <div className="h-1.5 rounded-full" style={{ width: `${Math.min(100, value)}%`, background: color }} />;
}

export default function DashboardPage() {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    getDashboardMetrics()
      .then(setMetrics)
      .catch(() => setError('Unable to load dashboard metrics. Please try again later.'))
      .finally(() => setLoading(false));
  }, []);

  const activityMax = useMemo(() => {
    if (!metrics || metrics.activitySeries.length === 0) return 1;
    return Math.max(...metrics.activitySeries.map((point) => Math.max(point.created, point.completed)), 1);
  }, [metrics]);

  if (loading) {
    return <div className="rounded-3xl bg-white p-6 shadow-card">Loading dashboard...</div>;
  }

  if (error) {
    return (
      <div className="rounded-3xl border border-rose-100 bg-rose-50 p-6 text-rose-800 shadow-card">
        <h2 className="text-lg font-semibold">Dependency unavailable</h2>
        <p>{error}</p>
      </div>
    );
  }

  if (!metrics) {
    return null;
  }

  return (
    <div className="space-y-6">
      <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-card">
        <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.28em] text-slate-500">Dashboard</p>
            <h1 className="mt-2 text-3xl font-semibold text-slate-900">Team performance overview</h1>
            <p className="mt-2 max-w-2xl text-sm text-slate-500">
              Review real task status, upcoming deadlines, and recent activity from the central task database.
            </p>
          </div>
          <div className="rounded-3xl bg-slate-50 px-4 py-3 text-sm font-semibold text-slate-700">
            {metrics.completionRate}% complete this sprint
          </div>
        </div>
      </div>

      <div className="grid gap-5 xl:grid-cols-4">
        {[
          { label: 'Total Tasks', value: metrics.totalTasks, tone: 'bg-sky-50 text-sky-700', progress: 85 },
          { label: 'Completed', value: metrics.completedTasks, tone: 'bg-emerald-50 text-emerald-700', progress: metrics.completionRate },
          { label: 'Pending', value: metrics.pendingTasks, tone: 'bg-amber-50 text-amber-700', progress: 70 },
          { label: 'Overdue', value: metrics.overdueTasks, tone: 'bg-rose-50 text-rose-700', progress: 22 },
        ].map((card) => (
          <div key={card.label} className="rounded-3xl border border-slate-200 bg-white p-6 shadow-card">
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="text-xs uppercase tracking-[0.28em] text-slate-500">{card.label}</p>
                <p className="mt-4 text-3xl font-semibold text-slate-900">{card.value}</p>
              </div>
              <span className={`rounded-full px-3 py-1 text-sm font-medium ${card.tone}`}>{card.label === 'Completed' ? 'On track' : 'Live'}</span>
            </div>
            <div className="mt-6 rounded-full bg-slate-100 p-1">
              <StatBar color={card.label === 'Overdue' ? '#ef4444' : card.label === 'Pending' ? '#f59e0b' : card.label === 'Completed' ? '#10b981' : '#2563eb'} value={card.progress} />
            </div>
          </div>
        ))}
      </div>

      <div className="grid gap-5 xl:grid-cols-[2fr_1fr]">
        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-card">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-sm uppercase tracking-[0.28em] text-slate-500">Productivity</p>
              <h2 className="mt-2 text-xl font-semibold text-slate-900">Tasks created vs completed</h2>
            </div>
            <div className="rounded-full border border-slate-200 bg-slate-50 px-4 py-2 text-sm font-semibold text-slate-700">
              {metrics.completionRate}% completion rate
            </div>
          </div>
          <div className="mt-6">
            <div className="grid grid-cols-2 gap-4 text-sm text-slate-500">
              <div className="flex items-center gap-3">
                <span className="h-2.5 w-2.5 rounded-full bg-sky-600" /> Created
              </div>
              <div className="flex items-center gap-3">
                <span className="h-2.5 w-2.5 rounded-full bg-emerald-500" /> Completed
              </div>
            </div>
            <div className="mt-6 relative">
              <div className="pointer-events-none absolute inset-x-0 top-0 bottom-0 grid grid-rows-5">
                <div className="border-t border-slate-200/70" />
                <div className="border-t border-slate-200/70" />
                <div className="border-t border-slate-200/70" />
                <div className="border-t border-slate-200/70" />
                <div className="border-t border-slate-200/70" />
              </div>
              {metrics.activitySeries.length === 0 ? (
                <div className="relative col-span-7 rounded-2xl border border-dashed border-slate-200 bg-slate-50 p-4 text-sm text-slate-600">
                  No activity data is available yet for the productivity chart.
                </div>
              ) : (
                <div className="relative grid h-52 grid-cols-7 items-end gap-2">
                  {metrics.activitySeries.map((point) => {
                    const createdHeight = Math.round((point.created / activityMax) * 100);
                    const completedHeight = Math.round((point.completed / activityMax) * 100);

                    return (
                      <div key={point.date} className="flex h-full flex-col items-center gap-2 self-stretch">
                        <div className="flex h-full w-full flex-col justify-end gap-1">
                          <div
                            className="mx-auto w-4 rounded-full bg-sky-600"
                            style={{ height: point.created > 0 ? `${Math.max(createdHeight, 12)}%` : '0%' }}
                          />
                          <div
                            className="mx-auto w-4 rounded-full bg-emerald-500"
                            style={{ height: point.completed > 0 ? `${Math.max(completedHeight, 12)}%` : '0%' }}
                          />
                        </div>
                        <span className="text-[0.68rem] text-slate-500">{formatDay(point.date)}</span>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="space-y-5">
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-card">
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="text-sm uppercase tracking-[0.28em] text-slate-500">Upcoming deadlines</p>
                <h2 className="mt-2 text-xl font-semibold text-slate-900">Next 7 days</h2>
              </div>
              <span className="rounded-full bg-amber-50 px-3 py-1 text-sm font-medium text-amber-700">
                {metrics.upcomingDeadlines.length} tasks
              </span>
            </div>
            <div className="mt-6 space-y-4">
              {metrics.upcomingDeadlines.length === 0 ? (
                <p className="text-sm text-slate-600">No upcoming deadlines this week.</p>
              ) : (
                metrics.upcomingDeadlines.map((item) => (
                  <div key={item.taskId} className="rounded-3xl border border-slate-200 bg-slate-50 p-4">
                    <div className="flex items-center justify-between gap-3">
                      <div>
                        <p className="font-semibold text-slate-900">{item.title}</p>
                        <p className="text-xs uppercase tracking-[0.18em] text-slate-500 mt-1">{item.status.replace('_', ' ')}</p>
                      </div>
                      <span className="text-sm font-semibold text-slate-700">{new Date(item.dueDate).toLocaleDateString()}</span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-card">
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="text-sm uppercase tracking-[0.28em] text-slate-500">Recent activity</p>
                <h2 className="mt-2 text-xl font-semibold text-slate-900">Latest updates</h2>
              </div>
              <span className="rounded-full bg-slate-50 px-3 py-1 text-sm font-medium text-slate-700">
                {metrics.recentActivity.length}
              </span>
            </div>
            <div className="mt-6 space-y-4">
              {metrics.recentActivity.length === 0 ? (
                <p className="text-sm text-slate-600">No recent activity available yet.</p>
              ) : (
                metrics.recentActivity.map((item) => (
                  <div key={`${item.taskId}-${item.when}`} className="rounded-3xl border border-slate-200 bg-slate-50 p-4">
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <p className="font-semibold text-slate-900">{item.title}</p>
                        <p className="mt-1 text-sm text-slate-600">
                          {item.action} {item.status.replace('_', ' ')}
                        </p>
                      </div>
                      <span className="text-xs text-slate-500">{new Date(item.when).toLocaleDateString()}</span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          <Link to="/tasks/create" className="block rounded-2xl bg-sky-600 px-5 py-3 text-center text-sm font-semibold text-white shadow-sm transition hover:bg-sky-700">
            Create a new task
          </Link>
        </div>
      </div>
    </div>
  );
}
