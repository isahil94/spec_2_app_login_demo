import { apiClient } from './client';
import type { ProfileData, SettingsData } from '../../types';

export const getProfile = async (userId: string) => {
  const response = await apiClient.get<{ data: ProfileData }>(`/users/${userId}/profile`);
  return response.data.data;
};

export const updateProfile = async (userId: string, payload: Partial<ProfileData>) => {
  const response = await apiClient.patch<{ data: ProfileData }>(`/users/${userId}/profile`, payload);
  return response.data.data;
};

export const changePassword = async (
  userId: string,
  currentPassword: string,
  newPassword: string
) => {
  const response = await apiClient.post<{ data: { message: string } }>(
    `/users/${userId}/change-password`,
    {
      currentPassword,
      newPassword,
    }
  );
  return response.data.data;
};

export const getSettings = async (userId: string) => {
  const response = await apiClient.get<{ data: SettingsData }>(`/users/${userId}/settings`);
  return response.data.data;
};

export const updateSettings = async (userId: string, payload: Partial<SettingsData>) => {
  const response = await apiClient.patch<{ data: SettingsData }>(`/users/${userId}/settings`, payload);
  return response.data.data;
};
