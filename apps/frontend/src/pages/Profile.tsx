import { useEffect, useState } from 'react';
import { useAppSelector } from '../state/hooks';
import Button from '../components/Button';
import { changePassword, getProfile, updateProfile } from '../services/api/user';
import type { ProfileData } from '../types';

export default function ProfilePage() {
  const userId = useAppSelector((state) => state.auth.userId);
  const authFullName = useAppSelector((state) => state.auth.fullName);
  const [profile, setProfile] = useState<ProfileData | null>(null);
  const [dependencyError, setDependencyError] = useState<string | null>(null);
  const [fullName, setFullName] = useState('');
  const [contactInformation, setContactInformation] = useState('');
  const [contactError, setContactError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const [passwordSaving, setPasswordSaving] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [passwordMessage, setPasswordMessage] = useState<string | null>(null);
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [passwordError, setPasswordError] = useState<string | null>(null);

  useEffect(() => {
    if (!userId) return;
    getProfile(userId)
      .then((data) => {
        setProfile(data);
        setFullName(data.fullName || authFullName || '');
        setContactInformation(data.contactInformation ?? '');
        setDependencyError(null);
      })
      .catch(() => {
        setProfile(null);
        setFullName(authFullName || '');
        setDependencyError('Unable to load profile at this time. Some data may be stale.');
      });
  }, [authFullName, userId]);

  const validateContactInformation = () => {
    const emailRegex = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
    const phoneRegex = /^\+?[0-9\s\-()]{7,20}$/;

    if (!contactInformation.trim()) {
      setContactError(null);
      return true;
    }

    if (!emailRegex.test(contactInformation) && !phoneRegex.test(contactInformation)) {
      setContactError('Contact information must be a valid email address or phone number.');
      return false;
    }

    setContactError(null);
    return true;
  };

  const handleSave = async () => {
    if (!userId) return;
    if (!validateContactInformation()) return;
    setSaving(true);
    setMessage(null);
    try {
      const updated = await updateProfile(userId, {
        fullName,
        contactInformation,
      });
      setProfile(updated);
      setMessage('Profile updated successfully.');
    } catch {
      setMessage('Unable to update profile at this time.');
    } finally {
      setSaving(false);
    }
  };


  const handleChangePassword = async () => {
    if (!userId) return;
    if (newPassword.length < 8) {
      setPasswordError('New password must be at least 8 characters.');
      return;
    }
    if (newPassword !== confirmPassword) {
      setPasswordError('New password and confirmation must match.');
      return;
    }

    setPasswordSaving(true);
    setPasswordError(null);
    setPasswordMessage(null);

    try {
      await changePassword(userId, currentPassword, newPassword);
      setPasswordMessage('Password changed successfully.');
      setCurrentPassword('');
      setNewPassword('');
      setConfirmPassword('');
    } catch {
      setPasswordError('Unable to change password. Check your current password and try again.');
    } finally {
      setPasswordSaving(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-card">
        <h1 className="text-2xl font-semibold text-slate-900">Profile</h1>
        <p className="mt-2 text-sm text-slate-600">Review and update your personal account details.</p>
      </div>

      {dependencyError ? (
        <div className="rounded-3xl border border-rose-100 bg-rose-50 p-6 text-rose-800 shadow-card">
          <h2 className="text-lg font-semibold">Dependency unavailable</h2>
          <p>{dependencyError}</p>
        </div>
      ) : null}

      <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-card">
        <div className="space-y-6">
            <div className="grid gap-6 md:grid-cols-2">
              <div>
                <label className="block text-sm font-medium text-slate-700">Display Name</label>
                <input
                  type="text"
                  value={fullName}
                  onChange={(event) => setFullName(event.target.value)}
                  className="mt-2 w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700">Contact Information</label>
                <input
                  type="text"
                  value={contactInformation}
                  onChange={(event) => {
                    setContactInformation(event.target.value);
                    setContactError(null);
                  }}
                  onBlur={validateContactInformation}
                  className="mt-2 w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
                  placeholder="Enter email or phone number"
                />
                {contactError ? <p className="mt-2 text-sm text-rose-600">{contactError}</p> : null}
              </div>
            </div>
            <div className="mt-6 flex items-center gap-3">
              <Button type="button" onClick={handleSave} disabled={saving}>
                {saving ? 'Saving...' : 'Save Profile'}
              </Button>
              {message ? <p className="text-sm text-slate-600">{message}</p> : null}
            </div>
          </div>
        </div>

      <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-card">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.28em] text-slate-500">Security</p>
            <h2 className="mt-2 text-xl font-semibold text-slate-900">Change Password</h2>
          </div>
          <p className="text-sm text-slate-500">Passwords must be at least 8 characters.</p>
        </div>
        <div className="mt-6 grid gap-6 md:grid-cols-2">
          <div>
            <label className="block text-sm font-medium text-slate-700">Current Password</label>
            <input
              type="password"
              value={currentPassword}
              onChange={(event) => setCurrentPassword(event.target.value)}
              className="mt-2 w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
              placeholder="Enter current password"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700">New Password</label>
            <input
              type="password"
              value={newPassword}
              onChange={(event) => setNewPassword(event.target.value)}
              className="mt-2 w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
              placeholder="Enter new password"
            />
          </div>
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-slate-700">Confirm New Password</label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(event) => setConfirmPassword(event.target.value)}
              className="mt-2 w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
              placeholder="Confirm new password"
            />
          </div>
        </div>

        <div className="mt-6 flex flex-col gap-3 sm:flex-row sm:items-center">
          <Button type="button" onClick={handleChangePassword} disabled={passwordSaving}>
            {passwordSaving ? 'Updating...' : 'Change Password'}
          </Button>
          {passwordError ? <p className="text-sm text-rose-600">{passwordError}</p> : null}
          {passwordMessage ? <p className="text-sm text-emerald-600">{passwordMessage}</p> : null}
        </div>
      </div>
    </div>
  );
}
