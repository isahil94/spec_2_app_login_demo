import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getTasks, TaskListParams } from '../services/api/tasks';
import type { TaskListItem } from '../types';
import Button from '../components/Button';

const statusOptions = [
  { label: 'All statuses', value: '' },
  { label: 'Todo', value: 'todo' },
  { label: 'In Progress', value: 'in_progress' },
  { label: 'Review', value: 'review' },
  { label: 'Completed', value: 'completed' },
  { label: 'Blocked', value: 'blocked' }
];

const priorityOptions = [
  { label: 'All priorities', value: '' },
  { label: 'Low', value: 'low' },
  { label: 'Medium', value: 'medium' },
  { label: 'High', value: 'high' },
  { label: 'Critical', value: 'critical' }
];

const statusStyles: Record<string, string> = {
  todo: 'bg-slate-100 text-slate-700',
  in_progress: 'bg-sky-100 text-sky-700',
  review: 'bg-amber-100 text-amber-700',
  completed: 'bg-emerald-100 text-emerald-700',
  blocked: 'bg-rose-100 text-rose-700'
};

const priorityStyles: Record<string, string> = {
  low: 'bg-emerald-100 text-emerald-700',
  medium: 'bg-amber-100 text-amber-700',
  high: 'bg-orange-100 text-orange-700',
  critical: 'bg-rose-100 text-rose-700'
};

export default function TaskListPage() {
  const [tasks, setTasks] = useState<TaskListItem[]>([]);
  const [search, setSearch] = useState('');
  const [status, setStatus] = useState('');
  const [priority, setPriority] = useState('');
  const [sort, setSort] = useState('recently_updated');
  const [page, setPage] = useState(1);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [hasMore, setHasMore] = useState(false);
  const limit = 6;

  const loadTasks = async (params: TaskListParams = {}) => {
    setError(null);
    setLoading(true);
    try {
      const response = await getTasks(params);
      setTasks(response);
      setHasMore(response.length === limit);
    } catch {
      setError('Unable to load tasks. Please check your connection or try again later.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setPage(1);
  }, [search, status, priority, sort]);

  useEffect(() => {
    loadTasks({ search, status, priority, sort, order: 'asc', page, limit });
  }, [search, status, priority, sort, page]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 rounded-3xl border border-slate-200 bg-white p-6 shadow-card md:flex-row md:items-end md:justify-between">
        <div className="grid flex-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
          <label className="block text-sm font-medium text-slate-700">
            Search
            <input
              type="search"
              placeholder="Search tasks"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              className="mt-2 w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 text-sm text-slate-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
            />
          </label>
          <label className="block text-sm font-medium text-slate-700">
            Status
            <select
              value={status}
              onChange={(event) => setStatus(event.target.value)}
              className="mt-2 w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
            >
              {statusOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </label>
          <label className="block text-sm font-medium text-slate-700">
            Priority
            <select
              value={priority}
              onChange={(event) => setPriority(event.target.value)}
              className="mt-2 w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
            >
              {priorityOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </label>
        </div>
        <div className="flex items-center gap-3">
          <label className="block text-sm font-medium text-slate-700">
            Sort
            <select
              value={sort}
              onChange={(event) => setSort(event.target.value)}
              className="mt-2 rounded-2xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
            >
              <option value="recently_updated">Recently updated</option>
              <option value="due_date">Due date</option>
              <option value="priority">Priority</option>
              <option value="status">Status</option>
            </select>
          </label>
          <Link to="/tasks/create">
            <Button type="button">Create Task</Button>
          </Link>
        </div>
      </div>
      {loading ? (
        <div className="rounded-3xl bg-white p-6 shadow-card">Loading tasks...</div>
      ) : error ? (
        <div className="rounded-3xl border border-rose-100 bg-rose-50 p-6 text-rose-800 shadow-card">
          <h2 className="text-lg font-semibold">Dependency unavailable</h2>
          <p>{error}</p>
        </div>
      ) : tasks.length === 0 ? (
        <div className="rounded-3xl border border-slate-200 bg-white p-6 text-slate-700 shadow-card">
          <p className="text-sm">No tasks match your current search and filters.</p>
        </div>
      ) : (
        <div className="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-card">
          <table className="min-w-full divide-y divide-slate-200">
            <thead className="bg-slate-50 text-left text-sm uppercase tracking-[0.12em] text-slate-500">
              <tr>
                <th className="px-6 py-4">Task</th>
                <th className="px-6 py-4">Status</th>
                <th className="px-6 py-4">Priority</th>
                <th className="px-6 py-4">Assignee</th>
                <th className="px-6 py-4">Due</th>
                <th className="px-6 py-4">Updated</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 bg-white text-sm text-slate-700">
              {tasks.map((task) => (
                <tr key={task.taskId} className="hover:bg-slate-50">
                  <td className="px-6 py-4">
                    <Link to={`/tasks/${task.taskId}`} className="font-semibold text-slate-900 hover:text-slate-700">
                      {task.title}
                    </Link>
                  </td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.16em] ${statusStyles[task.status]}`}>
                      {task.status.replace('_', ' ')}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.16em] ${priorityStyles[task.priority]}`}>
                      {task.priority}
                    </span>
                  </td>
                  <td className="px-6 py-4">{task.assignee?.fullName ?? 'Unassigned'}</td>
                  <td className="px-6 py-4">{task.dueDate ?? '—'}</td>
                  <td className="px-6 py-4">{new Date(task.updatedAt).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="flex flex-col gap-3 border-t border-slate-200 bg-slate-50 px-6 py-4 sm:flex-row sm:items-center sm:justify-between">
            <p className="text-sm text-slate-600">
              Showing page {page} · {tasks.length} task{tasks.length === 1 ? '' : 's'}
            </p>
            <div className="flex items-center gap-2">
              <button
                type="button"
                disabled={page === 1}
                onClick={() => setPage((current) => Math.max(current - 1, 1))}
                className="inline-flex items-center justify-center rounded-2xl border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-40"
              >
                Previous
              </button>
              <button
                type="button"
                disabled={!hasMore}
                onClick={() => setPage((current) => current + 1)}
                className="inline-flex items-center justify-center rounded-2xl border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-40"
              >
                Next
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
