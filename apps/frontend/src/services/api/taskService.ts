export interface TaskSummary {
  task_id: string;
  title: string;
  status: string;
  priority: string;
  assignee_id?: string;
  due_date?: string;
}

export interface TaskDetail extends TaskSummary {
  description?: string;
  labels?: string[];
  creator_id?: string;
  created_at?: string;
  history_summary?: string;
  comments_count?: number;
}

import { authService } from './authService';

const API_BASE = 'http://127.0.0.1:8001/api/v1';

function authHeaders() {
  const token = authService.getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function fetchTasks(): Promise<TaskSummary[]> {
  const response = await fetch(`${API_BASE}/tasks`, { headers: { ...authHeaders() } });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || 'Unable to fetch tasks');
  }
  return response.json();
}

export async function fetchTask(taskId: string): Promise<TaskDetail> {
  const response = await fetch(`${API_BASE}/tasks/${taskId}`, { headers: { ...authHeaders() } });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || 'Unable to fetch task');
  }
  return response.json();
}

export async function createTask(payload: Partial<TaskDetail>): Promise<TaskDetail> {
  const response = await fetch(`${API_BASE}/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || 'Unable to create task');
  }
  return response.json();
}

export async function createComment(taskId: string, content: string) {
  const response = await fetch(`${API_BASE}/tasks/${taskId}/comments`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify({ content }),
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || 'Unable to add comment');
  }
  return response.json();
}
