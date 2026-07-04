import { FormEvent, useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { addTaskComment } from '../services/api/collaboration';
import { getTaskDetail } from '../services/api/tasks';
import type { TaskDetail } from '../types';

export default function TaskDetailsPage() {
  const { id } = useParams();
  const [task, setTask] = useState<TaskDetail | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [commentText, setCommentText] = useState('');
  const [commentError, setCommentError] = useState<string | null>(null);
  const [commentSubmitting, setCommentSubmitting] = useState(false);

  const loadTask = async (taskId: string) => {
    setError(null);
    setLoading(true);
    try {
      const data = await getTaskDetail(taskId);
      setTask(data);
    } catch {
      setError('Unable to load task details.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!id) return;
    void loadTask(id);
  }, [id]);

  const handleCommentSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setCommentError(null);
    if (!commentText.trim()) {
      setCommentError('Comment text is required.');
      return;
    }

    if (!id) {
      setCommentError('Task ID is missing.');
      return;
    }

    setCommentSubmitting(true);
    try {
      const comment = await addTaskComment(id, { content: commentText.trim() });
      setTask((prev) =>
        prev
          ? { ...prev, comments: [comment, ...prev.comments] }
          : prev
      );
      setCommentText('');
    } catch {
      setCommentError('Unable to post comment.');
    } finally {
      setCommentSubmitting(false);
    }
  };

  if (loading) {
    return <div className="rounded-3xl bg-white p-6 shadow-card">Loading task details...</div>;
  }

  if (error) {
    return (
      <div className="rounded-3xl border border-rose-100 bg-rose-50 p-6 text-rose-800 shadow-card">
        <h2 className="text-lg font-semibold">Dependency unavailable</h2>
        <p>{error}</p>
      </div>
    );
  }

  if (!task) {
    return null;
  }

  return (
    <div className="space-y-6">
      <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-card">
        <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-slate-900">{task.title}</h1>
            <p className="mt-1 text-sm text-slate-600">{task.description || 'No description provided.'}</p>
          </div>
          <div className="space-y-2 text-sm text-slate-500">
            <p>Status: <span className="font-medium text-slate-900">{task.status.replace('_', ' ')}</span></p>
            <p>Priority: <span className="font-medium text-slate-900">{task.priority}</span></p>
          </div>
        </div>
      </div>
      <div className="grid gap-4 lg:grid-cols-2">
        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-card">
          <h2 className="text-lg font-semibold text-slate-900">Task details</h2>
          <dl className="mt-4 space-y-3 text-sm text-slate-600">
            <div>
              <dt className="font-medium text-slate-800">Owner</dt>
              <dd>{task.owner.fullName || task.owner.email}</dd>
            </div>
            <div>
              <dt className="font-medium text-slate-800">Assignee</dt>
              <dd>{task.assignee?.fullName ?? 'Unassigned'}</dd>
            </div>
            <div>
              <dt className="font-medium text-slate-800">Due date</dt>
              <dd>{task.dueDate ?? 'Not set'}</dd>
            </div>
            <div>
              <dt className="font-medium text-slate-800">Created</dt>
              <dd>{new Date(task.createdAt).toLocaleString()}</dd>
            </div>
          </dl>
        </div>
        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-card">
          <h2 className="text-lg font-semibold text-slate-900">History</h2>
          <div className="mt-4 space-y-4 text-sm text-slate-700">
            {task.history.length === 0 ? (
              <p className="text-slate-600">No history entries available.</p>
            ) : (
              task.history.map((entry) => (
                <div key={`${entry.action}-${entry.timestamp}`} className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                  <p className="font-medium text-slate-900">{entry.action.replace('_', ' ')}</p>
                  <p className="text-slate-600">{new Date(entry.timestamp).toLocaleString()}</p>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
      <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-card">
        <h2 className="text-lg font-semibold text-slate-900">Comments</h2>
        <form className="mt-4 space-y-4" onSubmit={handleCommentSubmit}>
          <div>
            <label htmlFor="comment" className="block text-sm font-medium text-slate-700">
              Add a comment
            </label>
            <textarea
              id="comment"
              value={commentText}
              onChange={(event) => setCommentText(event.target.value)}
              rows={4}
              className="mt-2 w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
              placeholder="Describe your update or feedback"
            />
            {commentError ? <p className="mt-2 text-sm text-rose-600">{commentError}</p> : null}
          </div>
          <div className="flex items-center gap-3">
            <button
              type="submit"
              disabled={commentSubmitting}
              className="rounded-2xl bg-blue-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-400"
            >
              {commentSubmitting ? 'Posting...' : 'Post Comment'}
            </button>
          </div>
        </form>
        {task.comments.length === 0 ? (
          <p className="mt-4 text-sm text-slate-600">No comments yet.</p>
        ) : (
          <ul className="mt-4 space-y-4">
            {task.comments.map((comment) => (
              <li key={comment.commentId} className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                <p className="font-medium text-slate-900">{comment.author.fullName || comment.author.email}</p>
                <p className="mt-2 text-sm text-slate-700">{comment.content}</p>
                <p className="mt-2 text-xs text-slate-500">{new Date(comment.createdAt).toLocaleString()}</p>
              </li>
            ))}
          </ul>
        )}
      </div>
      <div className="flex flex-wrap items-center gap-3">
        <Link to="/tasks" className="text-sm font-medium text-blue-600 hover:underline">
          Back to task list
        </Link>
        <Link to={`/tasks/${task.taskId}`} className="text-sm font-medium text-slate-700 hover:underline">
          Refresh
        </Link>
        <Link to={`/tasks/${task.taskId}/edit`} className="rounded-2xl bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700">
          Edit Task
        </Link>
      </div>
    </div>
  );
}
