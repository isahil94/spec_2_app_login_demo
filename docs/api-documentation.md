# Task Management System - API Documentation

## Overview

The Task Management System API provides RESTful endpoints for managing tasks, comments, users, teams, and more. The API uses JSON for request/response bodies and JWT tokens for authentication.

**Base URL:** `http://localhost:8001/api/v1`

## Authentication

All endpoints (except `/auth/register` and `/auth/login`) require a Bearer token in the `Authorization` header.

```
Authorization: Bearer <access_token>
```

## Error Handling

All error responses follow this format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {},
    "timestamp": "2024-01-01T12:00:00Z",
    "requestId": "uuid"
  }
}
```

---

## Authentication Endpoints

### Register User

**POST** `/auth/register`

Create a new user account.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "full_name": "John Doe"
}
```

**Response (200):**
```json
{
  "data": {
    "userId": "uuid-here",
    "email": "user@example.com",
    "fullName": "John Doe",
    "role": "TEAM_MEMBER",
    "createdAt": "2024-01-01T12:00:00Z"
  }
}
```

---

### Login

**POST** `/auth/login`

Authenticate and get an access token.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response (200):**
```json
{
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "expiresIn": 3600,
    "user": {
      "userId": "uuid-here",
      "email": "user@example.com",
      "fullName": "John Doe",
      "role": "TEAM_MEMBER"
    }
  }
}
```

---

## Task Endpoints

### Create Task

**POST** `/tasks`

Create a new task.

**Headers:**
```
Authorization: Bearer <token>
```

**Request:**
```json
{
  "title": "Fix login bug",
  "description": "Users unable to login on mobile",
  "status": "todo",
  "priority": "high",
  "dueDate": "2024-01-15T00:00:00Z",
  "teamId": "team-uuid (optional)",
  "assigneeId": "user-uuid (optional)"
}
```

**Response (200):**
```json
{
  "data": {
    "taskId": "task-uuid",
    "title": "Fix login bug",
    "description": "Users unable to login on mobile",
    "status": "todo",
    "priority": "high",
    "ownerId": "user-uuid",
    "assigneeId": null,
    "teamId": "team-uuid",
    "dueDate": "2024-01-15T00:00:00Z",
    "createdAt": "2024-01-01T12:00:00Z",
    "updatedAt": "2024-01-01T12:00:00Z"
  }
}
```

---

### List Tasks

**GET** `/tasks`

Get all tasks for the current user with optional filtering.

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `status` (optional): Filter by status (todo, in_progress, review, completed, blocked)
- `priority` (optional): Filter by priority (low, medium, high, critical)
- `assigned_to_me` (optional): Boolean, filter to only assigned tasks
- `limit` (optional): Max number of tasks to return (default: 50)
- `offset` (optional): Pagination offset (default: 0)

**Response (200):**
```json
{
  "data": [
    {
      "taskId": "task-uuid",
      "title": "Fix login bug",
      "status": "in_progress",
      "priority": "high",
      "owner": {
        "userId": "user-uuid",
        "fullName": "Alice Johnson"
      },
      "assignee": {
        "userId": "user-uuid",
        "fullName": "Bob Smith"
      },
      "dueDate": "2024-01-15T00:00:00Z",
      "createdAt": "2024-01-01T12:00:00Z"
    }
  ],
  "meta": {
    "total": 1,
    "limit": 50,
    "offset": 0
  }
}
```

---

### Get Task Details

**GET** `/tasks/{taskId}`

Get detailed information about a specific task including comments and history.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "data": {
    "taskId": "task-uuid",
    "title": "Fix login bug",
    "description": "Users unable to login on mobile",
    "status": "in_progress",
    "priority": "high",
    "owner": {
      "userId": "user-uuid",
      "fullName": "Alice Johnson",
      "email": "alice@example.com"
    },
    "assignee": {
      "userId": "user-uuid",
      "fullName": "Bob Smith",
      "email": "bob@example.com"
    },
    "team": {
      "teamId": "team-uuid",
      "name": "Engineering"
    },
    "dueDate": "2024-01-15T00:00:00Z",
    "createdAt": "2024-01-01T12:00:00Z",
    "updatedAt": "2024-01-01T13:00:00Z",
    "comments": [
      {
        "commentId": "comment-uuid",
        "content": "Started investigating",
        "author": {
          "userId": "user-uuid",
          "fullName": "Bob Smith"
        },
        "createdAt": "2024-01-01T13:00:00Z"
      }
    ],
    "history": [
      {
        "action": "status_changed",
        "details": "Changed from 'todo' to 'in_progress'",
        "actor": {
          "userId": "user-uuid",
          "fullName": "Bob Smith"
        },
        "createdAt": "2024-01-01T13:00:00Z"
      }
    ]
  }
}
```

---

### Update Task

**PATCH** `/tasks/{taskId}`

Update task properties.

**Headers:**
```
Authorization: Bearer <token>
```

**Request:**
```json
{
  "title": "Fix login bug on mobile",
  "status": "in_progress",
  "priority": "critical",
  "assigneeId": "user-uuid",
  "dueDate": "2024-01-10T00:00:00Z"
}
```

**Response (200):**
```json
{
  "data": {
    "taskId": "task-uuid",
    "title": "Fix login bug on mobile",
    "status": "in_progress",
    "priority": "critical",
    "updatedAt": "2024-01-01T14:00:00Z"
  }
}
```

---

### Archive Task

**POST** `/tasks/{taskId}/archive`

Archive a task (soft delete).

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "data": {
    "taskId": "task-uuid",
    "status": "archived",
    "archivedAt": "2024-01-01T14:00:00Z"
  }
}
```

---

### Restore Task

**POST** `/tasks/{taskId}/restore`

Restore an archived task.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "data": {
    "taskId": "task-uuid",
    "status": "todo",
    "archivedAt": null
  }
}
```

---

### Duplicate Task

**POST** `/tasks/{taskId}/duplicate`

Create a copy of a task with a new title.

**Headers:**
```
Authorization: Bearer <token>
```

**Request:**
```json
{
  "title": "Fix login bug - Phase 2"
}
```

**Response (200):**
```json
{
  "data": {
    "taskId": "new-task-uuid",
    "title": "Fix login bug - Phase 2",
    "status": "todo",
    "priority": "high",
    "ownerId": "user-uuid",
    "createdAt": "2024-01-01T14:00:00Z"
  }
}
```

---

## Comment Endpoints

### Add Comment

**POST** `/tasks/{taskId}/comments`

Add a new comment to a task.

**Headers:**
```
Authorization: Bearer <token>
```

**Request:**
```json
{
  "content": "I've started investigating this issue. It seems to be related to OAuth token refresh."
}
```

**Response (200):**
```json
{
  "data": {
    "commentId": "comment-uuid",
    "taskId": "task-uuid",
    "content": "I've started investigating this issue...",
    "author": {
      "userId": "user-uuid",
      "fullName": "Bob Smith"
    },
    "createdAt": "2024-01-01T14:00:00Z"
  }
}
```

---

### Get Task Comments

**GET** `/tasks/{taskId}/comments`

Get all comments on a task.

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `limit` (optional): Max comments to return (default: 50)
- `offset` (optional): Pagination offset (default: 0)

**Response (200):**
```json
{
  "data": {
    "comments": [
      {
        "commentId": "comment-uuid",
        "taskId": "task-uuid",
        "content": "I've started investigating...",
        "author": {
          "userId": "user-uuid",
          "fullName": "Bob Smith",
          "email": "bob@example.com"
        },
        "createdAt": "2024-01-01T14:00:00Z"
      }
    ],
    "meta": {
      "total": 1,
      "limit": 50,
      "offset": 0
    }
  }
}
```

---

### Update Comment

**PATCH** `/tasks/{taskId}/comments/{commentId}`

Update a comment (only by author or admin).

**Headers:**
```
Authorization: Bearer <token>
```

**Request:**
```json
{
  "content": "Updated comment text"
}
```

**Response (200):**
```json
{
  "data": {
    "commentId": "comment-uuid",
    "content": "Updated comment text",
    "updatedAt": "2024-01-01T15:00:00Z"
  }
}
```

---

## User Endpoints

### Get User Profile

**GET** `/users/{userId}/profile`

Get a user's public profile information.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "data": {
    "userId": "user-uuid",
    "fullName": "Alice Johnson",
    "email": "alice@example.com",
    "contactInformation": "alice@company.com"
  }
}
```

---

### Update User Profile

**PATCH** `/users/{userId}/profile`

Update current user's profile (must be own profile).

**Headers:**
```
Authorization: Bearer <token>
```

**Request:**
```json
{
  "fullName": "Alice J. Johnson",
  "contactInformation": "alice.johnson@company.com"
}
```

**Response (200):**
```json
{
  "data": {
    "userId": "user-uuid",
    "fullName": "Alice J. Johnson",
    "email": "alice@example.com",
    "contactInformation": "alice.johnson@company.com"
  }
}
```

---

### Get User Settings

**GET** `/users/{userId}/settings`

Get current user's settings.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "data": {
    "userId": "user-uuid",
    "theme": "light",
    "language": "en",
    "timezone": "UTC",
    "privacy": "private",
    "notifications": {
      "inApp": true,
      "email": true
    }
  }
}
```

---

### Update User Settings

**PATCH** `/users/{userId}/settings`

Update current user's settings.

**Headers:**
```
Authorization: Bearer <token>
```

**Request:**
```json
{
  "theme": "dark",
  "language": "en",
  "timezone": "America/New_York",
  "privacy": "public",
  "notifications": {
    "inApp": true,
    "email": false
  }
}
```

**Response (200):**
```json
{
  "data": {
    "userId": "user-uuid",
    "theme": "dark",
    "language": "en",
    "timezone": "America/New_York",
    "privacy": "public",
    "notifications": {
      "inApp": true,
      "email": false
    }
  }
}
```

---

## Team Endpoints

### Create Team

**POST** `/teams`

Create a new team.

**Headers:**
```
Authorization: Bearer <token>
```

**Request:**
```json
{
  "name": "Engineering",
  "description": "Engineering team for product development"
}
```

**Response (200):**
```json
{
  "data": {
    "teamId": "team-uuid",
    "name": "Engineering",
    "description": "Engineering team for product development",
    "createdAt": "2024-01-01T12:00:00Z"
  }
}
```

---

### Get Team

**GET** `/teams/{teamId}`

Get team details and members.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "data": {
    "teamId": "team-uuid",
    "name": "Engineering",
    "description": "Engineering team for product development",
    "members": [
      {
        "userId": "user-uuid",
        "fullName": "Alice Johnson",
        "email": "alice@example.com",
        "role": "TEAM_LEAD"
      }
    ],
    "createdAt": "2024-01-01T12:00:00Z"
  }
}
```

---

### Add Team Member

**POST** `/teams/{teamId}/members`

Add a user to a team.

**Headers:**
```
Authorization: Bearer <token>
```

**Request:**
```json
{
  "userId": "user-uuid"
}
```

**Response (200):**
```json
{
  "data": {
    "teamId": "team-uuid",
    "members": [
      {
        "userId": "user-uuid",
        "fullName": "Alice Johnson"
      }
    ]
  }
}
```

---

## Health Check

### Health Check

**GET** `/health`

Check API health status (no authentication required).

**Response (200):**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

---

## Status Codes

- **200** - Success
- **201** - Created
- **400** - Bad request
- **401** - Unauthorized (missing/invalid token)
- **403** - Forbidden (insufficient permissions)
- **404** - Not found
- **409** - Conflict
- **500** - Internal server error

---

## Rate Limiting

Currently no rate limiting is enforced. In production, implement appropriate rate limits based on user roles and endpoints.

---

## Pagination

List endpoints support pagination via query parameters:
- `limit`: Maximum items per page (default: 50, max: 100)
- `offset`: Number of items to skip (default: 0)

Response includes pagination metadata:
```json
{
  "data": [...],
  "meta": {
    "total": 100,
    "limit": 50,
    "offset": 0
  }
}
```

---

## Testing

See [Integration Tests Guide](#integration-tests) for testing these endpoints.
