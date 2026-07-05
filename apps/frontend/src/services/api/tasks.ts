import { apiClient } from './client';
import type { TaskListItem, TaskDetail, TaskStatus, TaskPriority, CommentItem, TaskHistoryItem, UserSummary } from '../../types';

export interface TaskListParams {
  search?: string;
  status?: string;
  priority?: string;
  assignee?: string;
  team?: string;
  dueDate?: string;
  dueDateFrom?: string;
  dueDateTo?: string;
  createdDate?: string;
  sort?: string;
  order?: 'asc' | 'desc';
  page?: number;
  limit?: number;
}

const normalizeUserSummary = (user: any): UserSummary => ({
  userId: user?.user_id ?? user?.userId ?? '',
  email: user?.email ?? '',
  fullName: user?.full_name ?? user?.fullName ?? user?.email ?? '',
});

const normalizeTaskListItem = (task: any): TaskListItem => ({
  taskId: task.task_id,
  title: task.title,
  status: task.status,
  priority: task.priority,
  owner: normalizeUserSummary(task.owner),
  assignee: task.assignee ? normalizeUserSummary(task.assignee) : null,
  dueDate: task.due_date ?? null,
  updatedAt: task.updated_at,
});

const normalizeCommentItem = (comment: any): CommentItem => ({
  commentId: comment.comment_id,
  author: normalizeUserSummary(comment.author),
  content: comment.content,
  createdAt: comment.created_at,
  updatedAt: comment.updated_at ?? null,
});

const normalizeHistoryItem = (entry: any): TaskHistoryItem => ({
  action: entry.action,
  actor: normalizeUserSummary(entry.author ?? entry.user ?? {}),
  timestamp: entry.created_at ?? entry.timestamp,
  details: entry.details ?? null,
});

const normalizeTaskDetail = (task: any): TaskDetail => ({
  taskId: task.task_id,
  title: task.title,
  description: task.description,
  status: task.status,
  priority: task.priority,
  owner: normalizeUserSummary(task.owner ?? {}),
  assignee: task.assignee ? normalizeUserSummary(task.assignee) : null,
  dueDate: task.due_date ?? null,
  labels: task.labels ?? [],
  createdAt: task.created_at,
  updatedAt: task.updated_at,
  history: Array.isArray(task.history) ? task.history.map(normalizeHistoryItem) : [],
  comments: Array.isArray(task.comments) ? task.comments.map(normalizeCommentItem) : [],
});

export const getTasks = async (params: TaskListParams = {}) => {
  const response = await apiClient.get<{ data: { tasks: any[] } }>('/tasks', { params });
  return response.data.data.tasks.map(normalizeTaskListItem);
};

export const getTaskDetail = async (taskId: string) => {
  const response = await apiClient.get<{ data: any }>(`/tasks/${taskId}`);
  return normalizeTaskDetail(response.data.data);
};

export interface CreateTaskPayload {
  title: string;
  description?: string;
  status: TaskStatus;
  priority: TaskPriority;
  assigneeId?: string;
  dueDate?: string;
}

export const createTask = async (payload: CreateTaskPayload) => {
  const response = await apiClient.post<{ data: any }>('/tasks', payload);
  return normalizeTaskListItem(response.data.data);
};

export interface UpdateTaskPayload {
  title?: string;
  description?: string;
  status?: TaskStatus;
  priority?: TaskPriority;
  assigneeId?: string | null;
  dueDate?: string;
}

export const updateTask = async (taskId: string, payload: UpdateTaskPayload) => {
  const response = await apiClient.patch<{ data: any }>(`/tasks/${taskId}`, payload);
  return normalizeTaskDetail(response.data.data);
};
