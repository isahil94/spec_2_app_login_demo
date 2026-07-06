import type { SettingsData } from './types';

export type AppTheme = SettingsData['theme'];

const THEME_KEY = 'themePreference';

export const applyTheme = (theme: AppTheme) => {
  document.documentElement.setAttribute('data-theme', theme);
};

export const persistTheme = (theme: AppTheme) => {
  window.localStorage.setItem(THEME_KEY, theme);
};

export const loadTheme = (): AppTheme => {
  const stored = window.localStorage.getItem(THEME_KEY) as AppTheme | null;
  return stored ?? 'light';
};

export const initTheme = () => {
  const theme = loadTheme();
  applyTheme(theme);
};
