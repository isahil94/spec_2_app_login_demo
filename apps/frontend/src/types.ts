export type UserRole = 'ADMIN' | 'TEAM_LEAD' | 'TEAM_MEMBER';

export interface UserSummary {
  userId: string;
  email: string;
  fullName?: string;
}

export type TaskStatus = 'todo' | 'in_progress' | 'review' | 'completed' | 'blocked';
export type TaskPriority = 'low' | 'medium' | 'high' | 'critical';

export interface TaskHistoryItem {
  action: string;
  actor: UserSummary;
  timestamp: string;
  details: Record<string, unknown> | null;
}

export interface CommentItem {
  commentId: string;
  author: UserSummary;
  content: string;
  createdAt: string;
  updatedAt: string | null;
}

export interface TaskDetail {
  taskId: string;
  title: string;
  description?: string;
  status: TaskStatus;
  priority: TaskPriority;
  owner: UserSummary;
  assignee: UserSummary | null;
  dueDate: string | null;
  labels?: string[];
  createdAt: string;
  updatedAt: string;
  history: TaskHistoryItem[];
  comments: CommentItem[];
}

export interface DashboardChartPoint {
  date: string;
  created: number;
  completed: number;
}

export interface DashboardActivityItem {
  taskId: string;
  title: string;
  action: string;
  when: string;
  status: TaskStatus;
}

export interface DashboardDeadlineItem {
  taskId: string;
  title: string;
  dueDate: string;
  when: string;
  status: TaskStatus;
}

export interface DashboardMetrics {
  totalTasks: number;
  completedTasks: number;
  pendingTasks: number;
  overdueTasks: number;
  dueTodayTasks: number;
  completionRate: number;
  activitySeries: DashboardChartPoint[];
  recentActivity: DashboardActivityItem[];
  upcomingDeadlines: DashboardDeadlineItem[];
}

export interface TaskListItem {
  taskId: string;
  title: string;
  status: TaskStatus;
  priority: TaskPriority;
  owner: UserSummary;
  assignee: UserSummary | null;
  dueDate: string | null;
  updatedAt: string;
}

export interface ProfileData {
  userId: string;
  fullName: string;
  email: string;
  contactInformation?: string;
}

export interface TeamSummary {
  teamId: string;
  name: string;
  description: string;
  owner: {
    userId: string;
    fullName?: string;
    email?: string;
  };
  memberCount: number;
  createdAt: string;
}

export interface SettingsData {
  theme: 'light' | 'dark' | 'system';
  notifications: {
    inApp: boolean;
    email: boolean;
  };
  language: string;
  timezone: string;
  privacy: string;
}

export interface ApiError {
  error: {
    code: string;
    message: string;
    details?: {
      field?: string;
      issue?: string;
    };
    timestamp: string;
    requestId: string;
  };
}
