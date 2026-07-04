# Low-Level Design (LLD)

## Purpose
Define package structure, internal architectures, design patterns, and implementation details for the Task Management System.

## Metadata
- Version: 1.0
- Author: Solution Architect
- Date: 2026-07-04
- Status: Draft
- Artifact ID: LLD-001

---

## Package Structure

### Presentation Layer Packages

```
src/presentation/
├── screens/              # Page-level components
│   ├── Login.tsx
│   ├── Register.tsx
│   ├── Dashboard.tsx
│   ├── TaskList.tsx
│   ├── TaskDetails.tsx
│   ├── CreateTask.tsx
│   ├── EditTask.tsx
│   ├── Profile.tsx
│   └── Settings.tsx
│
├── components/          # Reusable UI components
│   ├── Header.tsx
│   ├── Sidebar.tsx
│   ├── Button.tsx
│   ├── Input.tsx
│   ├── Select.tsx
│   ├── Modal.tsx
│   ├── TaskCard.tsx
│   ├── TaskForm.tsx
│   ├── CommentSection.tsx
│   ├── MetricsCard.tsx
│   ├── Filter.tsx
│   ├── Pagination.tsx
│   └── DependencyUnavailable.tsx
│
├── hooks/              # Custom React hooks
│   ├── useAuth.ts
│   ├── useTasks.ts
│   ├── useNotifications.ts
│   ├── useLocalStorage.ts
│   └── useFetch.ts
│
├── routing/            # Navigation and route protection
│   ├── Router.tsx
│   ├── ProtectedRoute.tsx
│   ├── PublicRoute.tsx
│   ├── routes.config.ts
│   └── routeHelpers.ts
│
├── state/              # Redux store
│   ├── store.ts
│   ├── slices/
│   │   ├── authSlice.ts
│   │   ├── tasksSlice.ts
│   │   ├── uiSlice.ts
│   │   ├── notificationsSlice.ts
│   │   └── settingsSlice.ts
│   ├── selectors/
│   │   ├── authSelectors.ts
│   │   ├── taskSelectors.ts
│   │   └── uiSelectors.ts
│   └── middlewares/
│       ├── authMiddleware.ts
│       └── errorMiddleware.ts
│
└── styles/
    ├── globals.css
    ├── variables.css
    └── components/
        └── [component-specific styles]
```

---

### Business Layer Packages

```
src/business/
├── services/           # Domain services
│   ├── AuthService.ts
│   ├── TaskService.ts
│   ├── TeamService.ts
│   ├── CollaborationService.ts
│   ├── NotificationService.ts
│   ├── ReportingService.ts
│   ├── ValidationService.ts
│   └── AuditService.ts
│
├── dto/                # Data Transfer Objects
│   ├── UserDTO.ts
│   ├── TaskDTO.ts
│   ├── CommentDTO.ts
│   ├── NotificationDTO.ts
│   ├── TeamDTO.ts
│   └── types.ts
│
├── models/             # Domain models
│   ├── User.ts
│   ├── Task.ts
│   ├── Team.ts
│   ├── Comment.ts
│   ├── Notification.ts
│   └── TaskStatus.ts
│
├── validators/         # Business rule validators
│   ├── TaskValidator.ts
│   ├── UserValidator.ts
│   ├── TeamValidator.ts
│   └── CompositeValidator.ts
│
├── errors/             # Custom exceptions
│   ├── ValidationError.ts
│   ├── NotFoundError.ts
│   ├── UnauthorizedError.ts
│   ├── ConflictError.ts
│   ├── DependencyUnavailableError.ts
│   └── ApplicationError.ts
│
├── events/             # Domain events
│   ├── TaskCreatedEvent.ts
│   ├── TaskStatusChangedEvent.ts
│   ├── CommentAddedEvent.ts
│   ├── EventPublisher.ts
│   └── EventSubscriber.ts
│
├── mappers/            # DTO mapping
│   ├── UserMapper.ts
│   ├── TaskMapper.ts
│   ├── CommentMapper.ts
│   └── NotificationMapper.ts
│
└── ports/              # Repository interfaces
    ├── IUserRepository.ts
    ├── ITaskRepository.ts
    ├── ITeamRepository.ts
    ├── ICommentRepository.ts
    ├── INotificationRepository.ts
    └── IAuditRepository.ts
```

---

### Data Layer Packages

```
src/data/
├── repositories/       # Repository implementations
│   ├── UserRepository.ts
│   ├── TaskRepository.ts
│   ├── TeamRepository.ts
│   ├── CommentRepository.ts
│   ├── NotificationRepository.ts
│   ├── AuditRepository.ts
│   └── BaseRepository.ts
│
├── database/           # Database setup
│   ├── connection.ts
│   ├── ConnectionPool.ts
│   ├── seedData.ts
│   └── migrations/
│       ├── 001_init_schema.ts
│       ├── 002_audit_log.ts
│       ├── 003_indexes.ts
│       └── migration.interface.ts
│
├── queries/            # SQL and query builders
│   ├── userQueries.ts
│   ├── taskQueries.ts
│   ├── teamQueries.ts
│   ├── commentQueries.ts
│   ├── notificationQueries.ts
│   ├── auditQueries.ts
│   └── QueryBuilder.ts
│
└── orm/                # ORM configuration
    ├── entities/
    │   ├── UserEntity.ts
    │   ├── TaskEntity.ts
    │   ├── TeamEntity.ts
    │   ├── CommentEntity.ts
    │   ├── NotificationEntity.ts
    │   ├── AuditEntity.ts
    │   └── BaseEntity.ts
    └── decorators/
        ├── entity.ts
        ├── column.ts
        └── index.ts
```

---

### Shared (Cross-Cutting) Packages

```
src/shared/
├── logging/            # Structured logging
│   ├── Logger.ts
│   ├── LogEntry.ts
│   ├── transports/
│   │   ├── ConsoleTransport.ts
│   │   ├── FileTransport.ts
│   │   └── CloudTransport.ts
│   └── formatters/
│       ├── JSONFormatter.ts
│       └── TextFormatter.ts
│
├── config/             # Configuration management
│   ├── config.ts
│   ├── environment.ts
│   ├── validation.ts
│   ├── secrets.ts
│   └── schemas/
│       └── config.schema.ts
│
├── error-handling/     # Error handling infrastructure
│   ├── ErrorHandler.ts
│   ├── ErrorSerializer.ts
│   ├── DependencyUnavailable.ts
│   ├── ErrorMiddleware.ts
│   └── ErrorRecovery.ts
│
├── auth/               # Authentication & session
│   ├── JWTProvider.ts
│   ├── SessionManager.ts
│   ├── TokenValidator.ts
│   ├── PasswordHasher.ts
│   └── RoleValidator.ts
│
├── cache/              # Caching layer
│   ├── Cache.interface.ts
│   ├── MemoryCache.ts
│   ├── RedisCache.ts
│   ├── CacheKey.ts
│   └── CacheInvalidation.ts
│
├── constants/          # Application constants
│   ├── statusValues.ts
│   ├── priorityValues.ts
│   ├── roles.ts
│   ├── permissions.ts
│   ├── errorCodes.ts
│   └── messages.ts
│
├── utils/              # Utility functions
│   ├── dateUtils.ts
│   ├── stringUtils.ts
│   ├── arrayUtils.ts
│   ├── objectUtils.ts
│   ├── typeGuards.ts
│   └── validationUtils.ts
│
├── decorators/         # TypeScript decorators
│   ├── Cached.ts
│   ├── Validated.ts
│   ├── Authorized.ts
│   ├── Logged.ts
│   └── Retry.ts
│
└── middleware/         # HTTP middleware
    ├── AuthMiddleware.ts
    ├── LoggingMiddleware.ts
    ├── ErrorMiddleware.ts
    ├── ValidationMiddleware.ts
    ├── RateLimitMiddleware.ts
    └── CORSMiddleware.ts
```

---

## Design Patterns

### Dependency Injection
```typescript
// Constructor injection pattern
class TaskService {
  constructor(
    private taskRepository: ITaskRepository,
    private auditService: AuditService,
    private validationService: ValidationService,
    private notificationService: NotificationService,
    private logger: Logger
  ) {}
}

// Container registration
const container = new Container();
container.register<ITaskRepository>(
  'ITaskRepository',
  { useClass: TaskRepository }
);
container.register<TaskService>('TaskService', {
  useFactory: (c) => new TaskService(
    c.resolve<ITaskRepository>('ITaskRepository'),
    c.resolve<AuditService>('AuditService'),
    // ... other dependencies
  )
});
```

### Repository Pattern
```typescript
interface IRepository<T> {
  create(entity: T): Promise<T>;
  findById(id: string): Promise<T | null>;
  update(id: string, entity: Partial<T>): Promise<T>;
  delete(id: string): Promise<void>;
  find(filter: Filter<T>): Promise<T[]>;
}

class TaskRepository implements IRepository<Task> {
  async find(filter: TaskFilter): Promise<Task[]> {
    return this.database
      .query('SELECT * FROM tasks')
      .where('owner_id', filter.owner)
      .where('status', filter.status)
      .orderBy('created_at', 'DESC')
      .limit(filter.limit)
      .offset(filter.offset);
  }
}
```

### Service Locator (Minimized)
```typescript
class ServiceContainer {
  private services = new Map<string, any>();
  
  register<T>(key: string, factory: () => T): void {
    this.services.set(key, factory);
  }
  
  resolve<T>(key: string): T {
    const factory = this.services.get(key);
    return factory();
  }
}
```

### Error Handling Pattern
```typescript
// Custom error hierarchy
class ApplicationError extends Error {
  constructor(
    public code: string,
    message: string,
    public statusCode: number = 500
  ) {
    super(message);
  }
}

class ValidationError extends ApplicationError {
  constructor(message: string, public fields?: Record<string, string>) {
    super('INVALID_INPUT', message, 400);
  }
}

// Usage in service
try {
  const result = await this.taskRepository.create(input);
} catch (error) {
  if (error instanceof ValidationError) {
    throw error; // Re-throw application error
  }
  throw new ApplicationError(
    'DEPENDENCY_UNAVAILABLE',
    'Database connection failed',
    503
  );
}
```

### Decorator Pattern
```typescript
// Logging decorator
function Logged(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
  const originalMethod = descriptor.value;
  descriptor.value = async function(...args: any[]) {
    logger.info(`Calling ${propertyKey}`, { args });
    const result = await originalMethod.apply(this, args);
    logger.info(`${propertyKey} completed`, { result });
    return result;
  };
}

// Authorization decorator
function Authorized(roles: string[]) {
  return function(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;
    descriptor.value = function(...args: any[]) {
      const user = getCurrentUser();
      if (!roles.includes(user.role)) {
        throw new UnauthorizedError('Access denied');
      }
      return originalMethod.apply(this, args);
    };
  };
}

// Usage
class TaskService {
  @Logged
  @Authorized(['ADMIN', 'TEAM_LEAD'])
  async deleteTask(id: string): Promise<void> {
    // Implementation
  }
}
```

### Observer/Event Pattern
```typescript
interface EventSubscriber<T> {
  handle(event: T): Promise<void>;
}

class EventPublisher<T> {
  private subscribers: EventSubscriber<T>[] = [];
  
  subscribe(subscriber: EventSubscriber<T>): void {
    this.subscribers.push(subscriber);
  }
  
  async publish(event: T): Promise<void> {
    await Promise.all(
      this.subscribers.map(s => s.handle(event))
    );
  }
}

// Usage
class TaskStatusChangedEvent {
  constructor(public taskId: string, public newStatus: TaskStatus) {}
}

class NotificationSubscriber implements EventSubscriber<TaskStatusChangedEvent> {
  async handle(event: TaskStatusChangedEvent): Promise<void> {
    // Send notification
  }
}
```

### Cache-Aside Pattern
```typescript
class ReportingService {
  private cache: Cache;
  
  async getDashboardMetrics(userId: string): Promise<DashboardMetrics> {
    const cacheKey = `dashboard_${userId}`;
    
    // Check cache
    let metrics = await this.cache.get(cacheKey);
    if (metrics) {
      return metrics;
    }
    
    // Cache miss - compute
    metrics = await this.computeMetrics(userId);
    
    // Store in cache (5-minute TTL)
    await this.cache.set(cacheKey, metrics, 300);
    
    return metrics;
  }
}
```

---

## Internal Workflows

### Task Creation Workflow
```
TaskService.createTask(input, userId)
  ├─ ValidationService.validateTaskInput(input)
  │   ├─ Title required and < 100 chars
  │   ├─ Status in allowed set
  │   ├─ Priority in allowed set
  │   └─ Due date not in past (BR-006)
  │
  ├─ Ownership assignment
  │   └─ Set owner = userId
  │
  ├─ TaskRepository.create(taskEntity)
  │   └─ Execute INSERT transaction
  │
  ├─ AuditService.recordEvent('TASK_CREATED')
  │   └─ Append audit entry
  │
  ├─ EventPublisher.publish(TaskCreatedEvent)
  │   └─ Notify subscribers (notifications, activity tracking)
  │
  └─ Return TaskDTO (mapped from entity)
```

### Task Status Update Workflow
```
TaskService.updateTaskStatus(taskId, newStatus, userId)
  ├─ TaskRepository.findById(taskId)
  │   └─ Load current task
  │
  ├─ Authorization checks
  │   ├─ User is owner OR assignee OR admin
  │   └─ If completed, must be admin (BR-004)
  │
  ├─ ValidationService.validateStatusTransition(current, newStatus)
  │   └─ Allowed transition (BR-007)
  │
  ├─ Optimistic locking check
  │   ├─ Load current version from DB
  │   ├─ If version mismatch → Conflict error
  │   └─ Increment version for update
  │
  ├─ TaskRepository.update(taskId, { status, version })
  │   └─ Execute UPDATE with version check
  │
  ├─ AuditService.recordEvent('TASK_STATUS_CHANGED')
  │   └─ Record before/after values
  │
  ├─ EventPublisher.publish(TaskStatusChangedEvent)
  │   └─ Trigger notifications
  │
  └─ Return updated TaskDTO
```

### Search Workflow
```
TaskService.listTasks(filter, userId)
  ├─ Authorization: Determine visible scope
  │   ├─ Admin: All tasks
  │   ├─ Team Lead: Team + own tasks
  │   └─ Member: Own + assigned + team
  │
  ├─ Build query
  │   ├─ Base WHERE: not archived (or include if filter specifies)
  │   ├─ Apply filters: status, priority, owner, assignee, team, due date
  │   ├─ Full-text search on title + description (if search term)
  │   └─ Sort by requested field
  │
  ├─ Execute paginated query
  │   ├─ Offset: (page - 1) * limit
  │   ├─ Limit: max 100
  │   └─ Get total count for pagination
  │
  ├─ AuditService.logSearchAction(userId, filter)
  │   └─ Log search usage for compliance
  │
  └─ Return paginated TaskDTO[]
```

---

## Error Propagation

```
HTTP Request
  ↓
AuthMiddleware
  ├─ Extract and validate token
  └─ If invalid → Return 401 Unauthorized
  ↓
Route Handler
  ├─ Call service method
  ├─ Service throws ApplicationError
  │   ├─ ValidationError → 400 Bad Request
  │   ├─ UnauthorizedError → 403 Forbidden
  │   ├─ NotFoundError → 404 Not Found
  │   ├─ ConflictError → 409 Conflict
  │   └─ DependencyUnavailableError → 503 Service Unavailable
  │
  └─ ErrorMiddleware
      ├─ Catch error
      ├─ Serialize to error response
      ├─ Log with full context
      └─ Return to client with status code
```

---

## Concurrency Control

### Optimistic Locking
```typescript
// Task entity includes version field
class TaskEntity {
  id: string;
  title: string;
  status: TaskStatus;
  version: number; // Incremented on each update
}

// Update with version check
async updateTask(id: string, updates: Partial<Task>, currentVersion: number) {
  const result = await this.database.query(
    'UPDATE tasks SET version = version + 1, ... WHERE id = ? AND version = ?',
    [id, currentVersion]
  );
  
  if (result.affectedRows === 0) {
    throw new ConflictError('Task was modified by another user');
  }
}

// Client includes version in update request
PATCH /tasks/123 {
  "status": "in_progress",
  "version": 5
}
```

---

## Data Mapping (DTO vs Entity)

```typescript
// Task entity (ORM)
class TaskEntity {
  id: string;
  title: string;
  description: string;
  status: TaskStatus;
  priority: TaskPriority;
  owner_id: string;
  assignee_id: string | null;
  team_id: string | null;
  due_date: Date | null;
  archived_at: Date | null;
  version: number;
  created_at: Date;
  updated_at: Date;
}

// Task DTO (API response)
class TaskDTO {
  taskId: string;
  title: string;
  description: string;
  status: string;
  priority: string;
  owner: UserDTO;
  assignee: UserDTO | null;
  dueDate: string | null;
  createdAt: string;
  updatedAt: string;
}

// Mapper
class TaskMapper {
  static toDTO(entity: TaskEntity, ownerUser: User): TaskDTO {
    return {
      taskId: entity.id,
      title: entity.title,
      // ... map other fields
      owner: UserMapper.toDTO(ownerUser),
      createdAt: entity.created_at.toISOString(),
    };
  }
}
```

---

## Document Control

- **Document ID:** LLD-001
- **Version:** 1.0
- **Author:** Solution Architect
- **Status:** Ready for Handoff
