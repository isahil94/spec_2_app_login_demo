import { apiClient } from './client';
import type {
  DashboardActivityItem,
  DashboardChartPoint,
  DashboardDeadlineItem,
  DashboardMetrics,
} from '../../types';

interface DashboardMetricsResponse {
  total_tasks?: number;
  completed_tasks?: number;
  pending_tasks?: number;
  overdue_tasks?: number;
  due_today_tasks?: number;
  completion_rate?: number;
  totalTasks?: number;
  completedTasks?: number;
  pendingTasks?: number;
  overdueTasks?: number;
  dueTodayTasks?: number;
  completionRate?: number;
  activity_series?: {
    date: string;
    created: number;
    completed: number;
  }[];
  recent_activity?: {
    task_id: string;
    title: string;
    action: string;
    when: string;
    status: string;
  }[];
  upcoming_deadlines?: {
    task_id: string;
    title: string;
    due_date: string;
    when: string;
    status: string;
  }[];
}

const normalizeActivityPoint = (point: any): DashboardChartPoint => ({
  date: point.date ?? point.day ?? '',
  created: Number(point.created ?? point.created_count ?? 0),
  completed: Number(point.completed ?? point.completed_count ?? 0),
});

const normalizeActivityItem = (item: any): DashboardActivityItem => ({
  taskId: item.task_id,
  title: item.title,
  action: item.action,
  when: item.when,
  status: item.status,
});

const normalizeDeadlineItem = (item: any): DashboardDeadlineItem => ({
  taskId: item.task_id,
  title: item.title,
  dueDate: item.due_date,
  when: item.when,
  status: item.status,
});

const normalizeDashboardMetrics = (metrics: DashboardMetricsResponse): DashboardMetrics => ({
  totalTasks:
    metrics.totalTasks ?? metrics.total_tasks ?? 0,
  completedTasks:
    metrics.completedTasks ?? metrics.completed_tasks ?? 0,
  pendingTasks:
    metrics.pendingTasks ?? metrics.pending_tasks ?? 0,
  overdueTasks:
    metrics.overdueTasks ?? metrics.overdue_tasks ?? 0,
  dueTodayTasks:
    metrics.dueTodayTasks ?? metrics.due_today_tasks ?? 0,
  completionRate:
    metrics.completionRate ?? metrics.completion_rate ?? 0,
  activitySeries: Array.isArray(metrics.activity_series)
    ? metrics.activity_series.map(normalizeActivityPoint)
    : [],
  recentActivity: Array.isArray(metrics.recent_activity)
    ? metrics.recent_activity.map(normalizeActivityItem)
    : [],
  upcomingDeadlines: Array.isArray(metrics.upcoming_deadlines)
    ? metrics.upcoming_deadlines.map(normalizeDeadlineItem)
    : [],
});

export const getDashboardMetrics = async () => {
  const response = await apiClient.get<{ data: DashboardMetricsResponse }>('/dashboard/metrics');
  return normalizeDashboardMetrics(response.data.data);
};
