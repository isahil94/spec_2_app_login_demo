# Security Architecture

## Purpose
Define security principles, controls, and defensive mechanisms for the Task Management System.

## Metadata
- Version: 1.0
- Author: Solution Architect
- Date: 2026-07-04
- Status: Draft
- Artifact ID: SEC-ARCH-001

---

## Security Principles

1. **Defense in Depth:** Multiple layers of security controls
2. **Least Privilege:** Users and services have minimum required permissions
3. **Fail Secure:** System fails securely (deny by default)
4. **Secure by Default:** Security enabled without additional configuration
5. **Audit Everything:** All security-relevant actions logged
6. **Encryption First:** Data in transit and at rest encrypted

---

## Authentication

### Mechanism: JWT (JSON Web Tokens)
- **Format:** Header.Payload.Signature (Base64 encoded)
- **Algorithm:** HS256 or RS256
- **Token Expiry:** 24 hours
- **Refresh Strategy:** Optional refresh token with 7-day expiry

### Sign-In Flow
```
User enters credentials
  ↓
Validate email format
  ↓
Lookup user by email
  ↓
Hash provided password, compare with stored hash
  ↓
If match:
  - Generate JWT with userId, email, role
  - Set token expiry to 24 hours
  - Return token to client
  - Audit: "USER_SIGNED_IN" event
  ↓
If no match:
  - Log failed attempt
  - Rate limit: 5 failures per 15 minutes
  - After 5 failures: Lock account for 15 minutes
  - Audit: "USER_LOGIN_FAILED" event
  - Return: Generic "Invalid credentials" message
```

### Password Requirements
- Minimum 8 characters
- No complexity requirements (encourages passphrases)
- Password history: Cannot reuse last 3 passwords
- Expiry: Optional (not enforced)

### Password Storage
- **Hash Algorithm:** bcrypt with cost factor 10
- **Never Logged:** Passwords excluded from all logs
- **Never Transmitted:** Except over HTTPS

### Session Management
- **Stateless:** Tokens validate without server-side session store
- **Revocation:** Token revocation list (TRL) for logout
- **Validation:** Verify token signature on every request
- **HttpOnly Cookies:** Optional storage to prevent XSS token theft

---

## Authorization

### Role-Based Access Control (RBAC)

Three roles with hierarchical permissions:

#### Administrator
- **Scope:** Full system access
- **Task Permissions:** 
  - Create, edit, delete, archive, restore any task
  - Force status transitions
  - Permanent delete tasks
- **User Permissions:** Create, edit, delete, disable, enable users
- **Team Permissions:** Create, edit, delete teams; manage all memberships
- **Reporting:** View all reports, system-wide
- **Audit:** View complete audit logs

#### Team Lead
- **Scope:** Team-assigned tasks + personal tasks
- **Task Permissions:**
  - Create tasks for team
  - Edit team tasks (by ownership/assignment)
  - Archive team tasks (not permanent delete)
  - Cannot edit completed tasks
- **User Permissions:** Manage team members (add/remove)
- **Reporting:** View team workload and productivity
- **Audit:** View team-scoped audit logs

#### Team Member
- **Scope:** Personal tasks + assigned tasks + team visibility
- **Task Permissions:**
  - Create personal tasks
  - Edit assigned tasks (status only if not completed)
  - Archive personal tasks (not delete)
  - Cannot edit completed tasks (except status if assignee)
- **User Permissions:** View own profile
- **Reporting:** View personal dashboard only
- **Audit:** View own activity

---

## Input Validation & Sanitization

### Validation Strategy
1. **Schema Validation:** Joi or Zod for type and format
2. **Business Rule Validation:** Custom validators for domain logic
3. **Contextual Validation:** Authorization checks (ownership, team, role)

### Examples

#### Email Validation
```
Format: /^[^\s@]+@[^\s@]+\.[^\s@]+$/
Uniqueness: Check database for existing email
Length: max 254 characters (RFC 5321)
```

#### Password Validation
```
Length: 8-100 characters
Allowed: Printable ASCII characters
Forbidden: None (allow all printable)
```

#### Title Validation
```
Length: 1-100 characters
Format: Any characters allowed
Uniqueness: Not required (can have duplicate titles)
```

#### Due Date Validation
```
Format: ISO 8601 date (YYYY-MM-DD)
Constraint: Must not be earlier than today (BR-006)
Timezone: Stored as UTC, converted to user timezone
```

#### Status Validation
```
Allowed values: todo, in_progress, review, completed, blocked
Transition validation: Only allowed transitions permitted
```

### Sanitization Strategy
1. **Output Encoding:** React escapes HTML by default
2. **Database Escaping:** ORM handles parameterized queries
3. **No HTML in Task Content:** Allow only plain text + newlines
4. **Comment Sanitization:** Strip potentially dangerous tags

### XSS Prevention
- **React:** Built-in escaping of {{ }} expressions
- **Server:** No HTML tags in response payloads
- **Headers:** Content-Security-Policy headers (CSP)

### SQL Injection Prevention
- **No Raw SQL:** All queries use ORM or parameterized statements
- **Prepared Statements:** Bind variables prevent injection
- **Input Types:** Type checking at schema validation level

---

## Data Protection

### Encryption in Transit
- **Protocol:** HTTPS only (TLS 1.2+)
- **Enforcement:** All traffic to/from server encrypted
- **Certificates:** Let's Encrypt or managed CA
- **HSTS:** Strict-Transport-Security header enabled

### Encryption at Rest
- **Passwords:** Hashed with bcrypt (salted)
- **Sensitive Fields:** Optional pgcrypto in PostgreSQL
- **PII:** Email, contact info encrypted (future phase)
- **Configuration:** Secrets stored in environment variables, not code

### Data Classification

| Data | Classification | Protection |
|------|-----------------|-----------|
| Passwords | Confidential | Hash (bcrypt), never logged |
| Email | PII | Encrypted in transit, indexed (searchable) |
| Task Content | Internal | Encrypted in transit, access controlled |
| Comments | Internal | Encrypted in transit, access controlled |
| Audit Logs | Internal | Encrypted in transit, immutable storage |
| User Settings | Internal | Encrypted in transit, personal access |

---

## Secrets Management

### Secrets
- Database password
- JWT signing key
- API keys for external services
- OAuth credentials (future)

### Storage
- **Local:** Environment variables (`.env` file, gitignored)
- **Production:** Secrets management service (AWS Secrets Manager, HashiCorp Vault, etc.)
- **CI/CD:** Masked in logs, passed as encrypted environment variables

### Rotation
- **Strategy:** Support key rotation without downtime
- **Frequency:** Annual rotation minimum
- **Implementation:** Multiple active keys during rotation window

---

## Access Control

### Endpoint Authorization
Every API endpoint validates authorization before processing:

```
POST /tasks/123
  ↓
Extract token from Authorization header
  ↓
Verify token signature and expiry
  ↓
Extract userId and role from payload
  ↓
Check operation against role permissions
  ↓
Check resource ownership (if applicable)
  ↓
Enforce business rules (completed task protection, etc.)
  ↓
If authorized: Process request
If not authorized: Return 403 Forbidden + audit log
```

### Audit Logging
Every authorization check logged:
- User ID
- Resource ID
- Action attempted
- Permission granted/denied
- Timestamp

---

## Error Handling & Information Disclosure

### Generic Error Messages
- **User Facing:** Generic message ("Access denied" not "Admin role required")
- **Server Side:** Detailed error logged with context
- **Security:** Don't leak implementation details, resource existence, etc.

### Examples

| Situation | User Message | Audit | Log Level |
|-----------|--------------|-------|-----------|
| Permission denied | "Access denied" | User + Resource + Action denied | INFO |
| Invalid credentials | "Invalid credentials" | Failed sign-in attempt | INFO |
| Concurrent edit conflict | "Another user edited this task" | Conflict detected | INFO |
| Database error | "Service temporarily unavailable" | Database connection failed | ERROR |
| Logic error | "Operation failed, please try again" | Unexpected error in service | ERROR |

---

## Account Lockout & Rate Limiting

### Account Lockout
- **Trigger:** 5 failed sign-in attempts
- **Duration:** 15 minutes
- **Override:** Admin can unlock immediately
- **Audit:** Lockout events logged

### Rate Limiting
- **Global:** 1000 requests per hour per user
- **Sign-In:** 5 attempts per 15 minutes per email
- **Search:** 100 searches per minute per user
- **Implementation:** Redis or in-memory counter
- **Response:** 429 Too Many Requests with Retry-After header

---

## Audit Logging

### Audited Events

**Authentication:**
- USER_SIGNED_IN (success)
- USER_SIGN_IN_FAILED (failure)
- USER_SIGNED_OUT
- PASSWORD_RECOVERY_INITIATED
- PASSWORD_RESET (success)
- ACCOUNT_LOCKED
- ACCOUNT_UNLOCKED

**Task Operations:**
- TASK_CREATED
- TASK_UPDATED (with field changes)
- TASK_STATUS_CHANGED
- TASK_ARCHIVED
- TASK_RESTORED
- TASK_DELETED (permanent, admin only)
- TASK_DUPLICATED

**Collaboration:**
- COMMENT_CREATED
- COMMENT_EDITED
- COMMENT_DELETED
- ATTACHMENT_UPLOADED
- ATTACHMENT_DELETED

**User Management:**
- USER_CREATED
- USER_ROLE_CHANGED
- USER_DISABLED
- USER_ENABLED
- USER_DELETED (permanent, admin only)

**Team Management:**
- TEAM_CREATED
- TEAM_UPDATED
- MEMBER_ADDED
- MEMBER_REMOVED

**Settings:**
- NOTIFICATION_PREFERENCE_CHANGED
- PROFILE_UPDATED
- PASSWORD_CHANGED

### Audit Entry Fields
```json
{
  "audit_id": "uuid",
  "timestamp": "2026-07-04T12:00:00Z",
  "actor_id": "user-uuid",
  "entity_type": "task",
  "entity_id": "task-uuid",
  "action": "TASK_UPDATED",
  "details": {
    "fields_changed": ["status", "priority"],
    "changes": {
      "status": { "from": "todo", "to": "in_progress" },
      "priority": { "from": "medium", "to": "high" }
    }
  },
  "ip_address": "192.168.1.1",
  "user_agent": "Mozilla/5.0...",
  "success": true
}
```

### Audit Access
- **Retention:** Indefinite (compliance requirement)
- **Immutable:** Append-only, no updates or deletes
- **Access:** Admins only
- **Export:** Support audit report export for compliance

---

## Threat Model

### High-Level Threats

| Threat | Mitigation |
|--------|-----------|
| Unauthorized access | RBAC, authentication, audit logging |
| Credential theft | HTTPS, HttpOnly cookies, JWT expiry, rate limiting |
| XSS attacks | Input validation, output escaping, CSP headers |
| SQL injection | Parameterized queries, ORM, input validation |
| CSRF attacks | CSRF tokens for state-changing operations (if cookies used) |
| Privilege escalation | Role validation, permission checks, audit logging |
| Data tampering | Task version fields, audit immutability |
| Account takeover | Password policy, rate limiting, account lockout |
| Information disclosure | Generic error messages, secure logging, HTTPS |
| Denial of service | Rate limiting, resource quotas, monitoring |

---

## Security Headers

```
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

---

## Compliance & Privacy

### Privacy Principles
- **Minimal Collection:** Collect only required data
- **Transparency:** Clear privacy policy on what data is retained
- **User Control:** Users can view and manage their data
- **Right to Delete:** Support account deletion (soft-delete, then hard-delete after retention period)

### GDPR Considerations
- **Consent:** Explicit opt-in for email notifications
- **Data Portability:** Export user data (future)
- **Right to Erasure:** Account deletion support
- **Data Minimization:** Limit PII collection
- **Audit Trails:** Support regulatory audits

---

## Security Testing

### Unit Tests
- Password validation rules
- Authorization checks on each service method
- Input validation edge cases

### Integration Tests
- End-to-end authentication flow
- Permission enforcement on API endpoints
- Rate limiting functionality

### Security Audit
- Annual third-party security review
- Penetration testing
- OWASP Top 10 validation
- Dependency vulnerability scanning

---

## Incident Response

### Security Incident Procedure
1. **Detect:** Monitor logs, alerts for suspicious activity
2. **Contain:** Disable compromised accounts, revoke tokens if needed
3. **Investigate:** Review audit logs to determine scope
4. **Remediate:** Fix vulnerability, patch code
5. **Notify:** Inform affected users if data breach
6. **Learn:** Post-incident review, update controls

### Contacts
- Security team lead (contact info in runbook)
- Incident response hotline
- Legal/compliance contact for breach disclosure

---

## Document Control

- **Document ID:** SEC-ARCH-001
- **Version:** 1.0
- **Author:** Solution Architect
- **Status:** Ready for Handoff
