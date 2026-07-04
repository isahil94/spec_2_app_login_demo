import { useEffect, useState } from 'react';
import { getTeams } from '../services/api/teams';
import type { TeamSummary } from '../types';

export default function TeamsPage() {
  const [teams, setTeams] = useState<TeamSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    getTeams()
      .then(setTeams)
      .catch(() => setError('Unable to load teams.'))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-6">
      <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-card">
        <h1 className="text-2xl font-semibold text-slate-900">Teams</h1>
        <p className="mt-2 text-sm text-slate-600">Review team membership and ownership for your organization.</p>
      </div>
      {loading ? (
        <div className="rounded-3xl bg-white p-6 shadow-card">Loading teams...</div>
      ) : error ? (
        <div className="rounded-3xl border border-rose-100 bg-rose-50 p-6 text-rose-800 shadow-card">
          <h2 className="text-lg font-semibold">Dependency unavailable</h2>
          <p>{error}</p>
        </div>
      ) : teams.length === 0 ? (
        <div className="rounded-3xl border border-slate-200 bg-white p-6 text-slate-700 shadow-card">
          <p className="text-sm">No teams are available for the current user.</p>
        </div>
      ) : (
        <div className="grid gap-4 xl:grid-cols-2">
          {teams.map((team) => (
            <div key={team.teamId} className="rounded-3xl border border-slate-200 bg-white p-6 shadow-card">
              <h2 className="text-xl font-semibold text-slate-900">{team.name}</h2>
              <p className="mt-2 text-sm text-slate-600">{team.description}</p>
              <div className="mt-4 text-sm text-slate-700">
                <p>
                  <span className="font-medium text-slate-900">Owner:</span> {team.owner.fullName || team.owner.email}
                </p>
                <p>
                  <span className="font-medium text-slate-900">Members:</span> {team.memberCount}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
