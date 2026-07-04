import { apiClient } from './client';
import type { TeamSummary } from '../../types';

export const getTeams = async () => {
  const response = await apiClient.get<{ data: { teams: TeamSummary[] } }>('/teams');
  return response.data.data.teams;
};
