import { apiClient } from './client';
import type { CommentItem } from '../../types';

export interface CommentPayload {
  content: string;
}

export interface CommentResponse {
  data: CommentItem;
}

const normalizeCommentItem = (comment: any): CommentItem => ({
  commentId: comment.comment_id ?? comment.commentId,
  author: {
    userId: comment.author?.user_id ?? comment.author?.userId,
    email: comment.author?.email,
    fullName: comment.author?.full_name ?? comment.author?.fullName,
  },
  content: comment.content,
  createdAt: comment.created_at ?? comment.createdAt,
  updatedAt: comment.updated_at ?? comment.updatedAt ?? null,
});

export const getTaskComments = async (taskId: string) => {
  const response = await apiClient.get<{ data: { comments: any[] } }>(`/tasks/${taskId}/comments`);
  return response.data.data.comments.map(normalizeCommentItem);
};

export const addTaskComment = async (taskId: string, payload: CommentPayload) => {
  const response = await apiClient.post<{ data: any }>(`/tasks/${taskId}/comments`, payload);
  return normalizeCommentItem(response.data.data);
};

export const uploadTaskAttachment = async (taskId: string, file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await apiClient.post<{ data: { filename: string } }>(`/tasks/${taskId}/attachments`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
  return response.data.data;
};
