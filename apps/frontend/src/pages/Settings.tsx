import { useEffect, useState } from 'react';
import { useAppSelector } from '../state/hooks';
import Button from '../components/Button';
import { getSettings, updateSettings } from '../services/api/user';
import { isDependencyUnavailable } from '../services/api/client';
import type { SettingsData } from '../types';
import { applyTheme, persistTheme } from '../theme';

const themeOptions = [
  { value: 'system', label: 'System' },
  { value: 'light', label: 'Light' },
  { value: 'dark', label: 'Dark' }
];

export default function SettingsPage() {
  const userId = useAppSelector((state) => state.auth.userId);
  const [settings, setSettings] = useState<SettingsData | null>(null);
  const [dependencyError, setDependencyError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    if (!userId) return;
    getSettings(userId)
      .then((s) => {
        setSettings(s);
        applyTheme(s.theme);
        persistTheme(s.theme);
        setDependencyError(null);
      })
      .catch((error) => {
        if (!isDependencyUnavailable(error)) {
          setDependencyError('Unable to load settings at this time.');
        } else {
          setDependencyError(null);
        }
      });
  }, [userId]);

  const handleSave = async () => {
    if (!userId || !settings) return;
    setSaving(true);
    try {
      const updated = await updateSettings(userId, settings);
      setSettings(updated);
      applyTheme(updated.theme);
      persistTheme(updated.theme);
      setMessage('Settings saved successfully.');
    } catch {
      setMessage('Unable to save settings at this time.');
    } finally {
      setSaving(false);
    }
  };

  const updateSetting = (field: keyof SettingsData, value: string | boolean | SettingsData['notifications']) => {
    if (field === 'theme') {
      const themeValue = value as SettingsData['theme'];
      applyTheme(themeValue);
      persistTheme(themeValue);
    }

    setSettings((current) => (current ? { ...current, [field]: value } : current));
  };

  if (!settings) {
    return dependencyError ? (
      <div className="rounded-3xl border border-rose-100 bg-rose-50 p-6 text-rose-800 shadow-card">
        <h2 className="text-lg font-semibold">Dependency unavailable</h2>
        <p>{dependencyError}</p>
      </div>
    ) : (
      <div className="rounded-3xl bg-white p-6 shadow-card">Loading settings...</div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-card">
        <h1 className="text-2xl font-semibold text-slate-900">Settings</h1>
        <p className="mt-2 text-sm text-slate-600">Update your preference and notification settings.</p>
      </div>
      <div className="grid gap-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-card md:grid-cols-2">
        <label className="block text-sm font-medium text-slate-700">
          Theme
          <select
            value={settings.theme}
            onChange={(event) => updateSetting('theme', event.target.value)}
            className="mt-2 w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
          >
            {themeOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </label>
        <label className="flex items-center gap-3 text-sm font-medium text-slate-700">
          <input
            type="checkbox"
            checked={settings.notifications.inApp}
            onChange={(event) => updateSetting('notifications', { ...settings.notifications, inApp: event.target.checked })}
            className="h-5 w-5 rounded border-slate-300 text-slate-900 focus:ring-blue-500"
          />
          In-app notifications
        </label>
        <label className="flex items-center gap-3 text-sm font-medium text-slate-700">
          <input
            type="checkbox"
            checked={settings.notifications.email}
            onChange={(event) => updateSetting('notifications', { ...settings.notifications, email: event.target.checked })}
            className="h-5 w-5 rounded border-slate-300 text-slate-900 focus:ring-blue-500"
          />
          Email notifications
        </label>
        <label className="block text-sm font-medium text-slate-700">
          Language
          <input
            type="text"
            value={settings.language}
            onChange={(event) => updateSetting('language', event.target.value)}
            className="mt-2 w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
          />
        </label>
        <label className="block text-sm font-medium text-slate-700">
          Time Zone
          <input
            type="text"
            value={settings.timezone}
            onChange={(event) => updateSetting('timezone', event.target.value)}
            className="mt-2 w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
          />
        </label>
        <label className="block text-sm font-medium text-slate-700">
          Privacy
          <input
            type="text"
            value={settings.privacy}
            onChange={(event) => updateSetting('privacy', event.target.value)}
            className="mt-2 w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
          />
        </label>
      </div>
      <div className="flex items-center gap-3">
        <Button type="button" onClick={handleSave} disabled={saving}>
          {saving ? 'Saving...' : 'Save Settings'}
        </Button>
        {message ? <p className="text-sm text-slate-600">{message}</p> : null}
      </div>
    </div>
  );
}
