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
  userId: user?.user_id ?? user?.userId ?? user?.id ?? '',
  email: user?.email ?? '',
  fullName:
    user?.full_name ?? user?.fullName ?? user?.name ?? user?.email ?? '',
});

const normalizeTaskListItem = (task: any): TaskListItem => ({
  taskId: task.task_id ?? task.taskId ?? task.id ?? '',
  title: task.title ?? task.name ?? '',
  status: task.status ?? 'todo',
  priority: task.priority ?? 'medium',
  owner: normalizeUserSummary(task.owner ?? {}),
  assignee: task.assignee ? normalizeUserSummary(task.assignee) : null,
  dueDate: task.due_date ?? task.dueDate ?? null,
  updatedAt: task.updated_at ?? task.updatedAt ?? '',
});

const normalizeCommentItem = (comment: any): CommentItem => ({
  commentId: comment.comment_id ?? comment.commentId ?? comment.id ?? '',
  author: normalizeUserSummary(comment.author ?? {}),
  content: comment.content ?? comment.body ?? '',
  createdAt: comment.created_at ?? comment.createdAt ?? '',
  updatedAt: comment.updated_at ?? comment.updatedAt ?? null,
});

const normalizeHistoryItem = (entry: any): TaskHistoryItem => ({
  action: entry.action ?? entry.type ?? '',
  actor: normalizeUserSummary(entry.author ?? entry.user ?? {}),
  timestamp:
    entry.created_at ?? entry.timestamp ?? entry.createdAt ?? entry.time ?? '',
  details: entry.details ?? entry.detail ?? null,
});

const normalizeTaskDetail = (task: any): TaskDetail => ({
  taskId: task.task_id ?? task.taskId ?? task.id ?? '',
  title: task.title ?? task.name ?? '',
  description: task.description ?? task.details ?? '',
  status: task.status ?? 'todo',
  priority: task.priority ?? 'medium',
  owner: normalizeUserSummary(task.owner ?? {}),
  assignee: task.assignee ? normalizeUserSummary(task.assignee) : null,
  dueDate: task.due_date ?? task.dueDate ?? null,
  labels: task.labels ?? task.tags ?? [],
  createdAt: task.created_at ?? task.createdAt ?? '',
  updatedAt: task.updated_at ?? task.updatedAt ?? '',
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
