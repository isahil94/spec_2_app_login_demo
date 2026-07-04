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

export default function TaskListPage() {
  const [tasks, setTasks] = useState<TaskListItem[]>([]);
  const [search, setSearch] = useState('');
  const [status, setStatus] = useState('');
  const [priority, setPriority] = useState('');
  const [sort, setSort] = useState('recently_updated');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const loadTasks = async (params: TaskListParams = {}) => {
    setError(null);
    setLoading(true);
    try {
      const response = await getTasks(params);
      setTasks(response);
    } catch {
      setError('Unable to load tasks. Please check your connection or try again later.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTasks({ search, status, priority, sort, order: 'asc', page: 1, limit: 20 });
  }, [search, status, priority, sort]);

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
                  <td className="px-6 py-4 capitalize">{task.status.replace('_', ' ')}</td>
                  <td className="px-6 py-4 capitalize">{task.priority}</td>
                  <td className="px-6 py-4">{task.assignee?.fullName ?? 'Unassigned'}</td>
                  <td className="px-6 py-4">{task.dueDate ?? '—'}</td>
                  <td className="px-6 py-4">{new Date(task.updatedAt).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
