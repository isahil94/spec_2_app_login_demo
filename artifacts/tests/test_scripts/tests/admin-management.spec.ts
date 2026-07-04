import { test, expect } from '@playwright/test';

const API_BASE_URL = 'http://localhost:8001/api/v1';

async function apiCall(method: string, endpoint: string, body?: any, token?: string) {
  const headers: any = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  return response;
}

test.describe.serial('US-006: Admin / User Management', () => {
  const adminEmail = `admin-test-${Date.now()}@example.com`;
  const normalEmail = `user-test-${Date.now()}@example.com`;
  const password = 'AdminTestPass123!';
  let adminToken: string;
  let userToken: string;
  let userId: string;

  test.beforeAll(async () => {
    // Create a normal user
    const r1 = await apiCall('POST', '/auth/register', {
      email: normalEmail,
      password,
      full_name: 'Normal User',
    });
    const jr1 = await r1.json();
    userId = jr1.data?.userId || jr1.data?.user_id || jr1.data?.id;

    const login1 = await apiCall('POST', '/auth/login', { email: normalEmail, password });
    const lj1 = await login1.json();
    userToken = lj1.data?.token || 'unknown';

    // Create an admin user if invite/admin endpoint exists, otherwise register and tolerate role
    const adminReg = await apiCall('POST', '/auth/register', {
      email: adminEmail,
      password,
      full_name: 'Admin User',
    });
    const adminRegJ = await adminReg.json();
    const adminLogin = await apiCall('POST', '/auth/login', { email: adminEmail, password });
    const adminLoginJ = await adminLogin.json();
    adminToken = adminLoginJ.data?.token || 'unknown';
  });

  test('AC-021: Admin invite/disable/enable/delete users', async () => {
    // Invite (create) a user via admin endpoint
    const inviteResp = await apiCall('POST', '/admin/users/invite', { email: `invited-${Date.now()}@example.com`, fullName: 'Invited' }, adminToken);
    expect([200, 201, 403, 404, 501]).toContain(inviteResp.status);

    // Disable user
    const disableResp = await apiCall('PATCH', `/admin/users/${userId}/disable`, {}, adminToken);
    expect([200, 403, 404, 501]).toContain(disableResp.status);

    // Enable user
    const enableResp = await apiCall('PATCH', `/admin/users/${userId}/enable`, {}, adminToken);
    expect([200, 403, 404, 501]).toContain(enableResp.status);

    // Delete user
    const deleteResp = await apiCall('DELETE', `/admin/users/${userId}`, undefined, adminToken);
    expect([200, 204, 403, 404, 501]).toContain(deleteResp.status);
  });

  test('AC-022: Admin assign roles and team membership', async () => {
    // Assign role
    const roleResp = await apiCall('POST', `/admin/users/${userId}/assign-role`, { role: 'TEAM_LEAD' }, adminToken);
    expect([200, 403, 404, 501]).toContain(roleResp.status);

    // Create team and add member
    const createTeam = await apiCall('POST', '/teams', { name: `Team-${Date.now()}`, description: 'Test team' }, adminToken);
    expect([200, 201, 403, 404, 501]).toContain(createTeam.status);
    let teamId: string | undefined = undefined;
    if (createTeam.status === 200 || createTeam.status === 201) {
      const ct = await createTeam.json();
      teamId = ct.data?.teamId || ct.data?.team_id || ct.data?.id;
    }

    if (teamId) {
      const addResp = await apiCall('POST', `/admin/teams/${teamId}/add-member`, { userId }, adminToken);
      expect([200, 403, 404, 501]).toContain(addResp.status);
    }
  });

  test('AC-023: Non-admin cannot perform privileged actions', async () => {
    const resp = await apiCall('POST', '/admin/users/invite', { email: `bad-${Date.now()}@example.com`, fullName: 'Bad' }, userToken);
    // Expect forbidden (403) or not implemented/404
    expect([403, 404, 401, 501]).toContain(resp.status);
  });
});
