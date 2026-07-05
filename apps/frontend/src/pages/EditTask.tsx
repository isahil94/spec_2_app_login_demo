import { FormEvent, useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import Button from '../components/Button';
import { getActiveUsers } from '../services/api/user';
import { getTaskDetail, updateTask } from '../services/api/tasks';
import type { TaskDetail, TaskPriority, TaskStatus, UserSummary } from '../types';

const statusOptions: TaskStatus[] = ['todo', 'in_progress', 'review', 'completed', 'blocked'];
const priorityOptions: TaskPriority[] = ['low', 'medium', 'high', 'critical'];

export default function EditTaskPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [task, setTask] = useState<TaskDetail | null>(null);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [status, setStatus] = useState<TaskStatus>('todo');
  const [priority, setPriority] = useState<TaskPriority>('medium');
  const [assignee, setAssignee] = useState('');
  const [users, setUsers] = useState<UserSummary[]>([]);
  const [userLoading, setUserLoading] = useState(true);
  const [userError, setUserError] = useState<string | null>(null);
  const [dueDate, setDueDate] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (!id) return;
    getTaskDetail(id)
      .then((taskData) => {
        setTask(taskData);
        setTitle(taskData.title);
        setDescription(taskData.description ?? '');
        setStatus(taskData.status);
        setPriority(taskData.priority);
        setAssignee(taskData.assignee?.userId ?? '');
        setDueDate(taskData.dueDate ?? '');
      })
      .catch(() => setError('Unable to load task details.'));
  }, [id]);

  useEffect(() => {
    setUserLoading(true);
    getActiveUsers()
      .then(setUsers)
      .catch((err) => {
        console.error('Failed to load assignees', err);
        setUserError('Unable to load assignees.');
      })
      .finally(() => setUserLoading(false));
  }, []);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setError(null);

    if (!title.trim()) {
      setError('Task title is required.');
      return;
    }

    if (title.length > 100) {
      setError('Task title must be 100 characters or fewer.');
      return;
    }

    if (dueDate && new Date(dueDate) < new Date(new Date().toISOString().split('T')[0])) {
      setError('Due date must not be earlier than today.');
      return;
    }

    if (!id) {
      setError('Task ID is missing.');
      return;
    }

    setSaving(true);
    try {
      await updateTask(id, {
        title,
        description,
        status,
        priority,
        assigneeId: assignee || undefined,
        dueDate: dueDate || undefined,
      });
      navigate(`/tasks/${id}`);
    } catch (error) {
      console.error('Task update failed', error);
      setError(error instanceof Error ? error.message : 'Unable to update task right now.');
    } finally {
      setSaving(false);
    }
  };

  if (!task) {
    return <div className="rounded-3xl bg-white p-6 shadow-card">Loading task...</div>;
  }

  return (
    <div>
      <h1 className="mb-4 text-2xl font-semibold text-slate-900">Edit Task</h1>
      <form className="space-y-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-card" onSubmit={handleSubmit}>
        <div className="grid gap-6 md:grid-cols-2">
          <label className="block text-sm font-medium text-slate-700">
            Title
            <input
              type="text"
              value={title}
              onChange={(event) => setTitle(event.target.value)}
              className="mt-2 w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
              required
              maxLength={100}
            />
          </label>
          <label className="block text-sm font-medium text-slate-700">
            Status
            <select
              value={status}
              onChange={(event) => setStatus(event.target.value as TaskStatus)}
              className="mt-2 w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
            >
              {statusOptions.map((value) => (
                <option key={value} value={value}>
                  {value.replace('_', ' ')}
                </option>
              ))}
            </select>
          </label>
        </div>
        <div className="grid gap-6 md:grid-cols-2">
          <label className="block text-sm font-medium text-slate-700">
            Priority
            <select
              value={priority}
              onChange={(event) => setPriority(event.target.value as TaskPriority)}
              className="mt-2 w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
            >
              {priorityOptions.map((value) => (
                <option key={value} value={value}>
                  {value}
                </option>
              ))}
            </select>
          </label>
          <label className="block text-sm font-medium text-slate-700">
            Assignee
            <select
              value={assignee}
              onChange={(event) => setAssignee(event.target.value)}
              disabled={userLoading}
              className="mt-2 w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
            >
              <option value="">Unassigned</option>
              {users.map((user) => (
                <option key={user.userId} value={user.userId}>
                  {user.fullName || user.email}
                </option>
              ))}
            </select>
            {userError ? <p className="mt-2 text-xs text-rose-600">{userError}</p> : null}
            {!userLoading && users.length === 0 ? (
              <p className="mt-2 text-xs text-slate-500">No assignable users available.</p>
            ) : null}
          </label>
        </div>
        <label className="block text-sm font-medium text-slate-700">
          Due Date
          <input
            type="date"
            value={dueDate}
            onChange={(event) => setDueDate(event.target.value)}
            className="mt-2 w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
          />
        </label>
        <label className="block text-sm font-medium text-slate-700">
          Description
          <textarea
            value={description}
            onChange={(event) => setDescription(event.target.value)}
            className="mt-2 min-h-[120px] w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
            maxLength={2000}
          />
        </label>
        {error ? <p className="text-sm text-rose-600">{error}</p> : null}
        <div className="flex flex-wrap items-center gap-3">
          <Button type="submit" disabled={saving}>
            {saving ? 'Updating...' : 'Save Changes'}
          </Button>
          <button type="button" className="text-sm font-medium text-slate-600 hover:text-slate-900" onClick={() => navigate(`/tasks/${id}`)}>
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}
