# Deployment Architecture

## Purpose
Define infrastructure, deployment strategy, and operational considerations for the Task Management System.

## Metadata
- Version: 1.0
- Author: Solution Architect
- Date: 2026-07-04
- Status: Draft
- Artifact ID: DEPLOY-ARCH-001

---

## Deployment Topology

```
┌──────────────────────────────────────────────────────────┐
│                   CLIENT LAYER                           │
├──────────────────────────────────────────────────────────┤
│  Web Browser (React SPA)                                 │
│  - Runs locally in browser                               │
│  - Communicates via HTTPS to API                         │
│  - Caches session token (JWT)                            │
└────────────────────┬─────────────────────────────────────┘
                     │
        ┌────────────▼─────────────┐
        │   CDN (Optional)         │
        │ - Static asset delivery  │
        │ - Geographically close   │
        └────────────┬─────────────┘
                     │
        ┌────────────▼─────────────────────┐
        │     SSL/TLS Termination          │
        │  (Reverse Proxy - Nginx/ALB)     │
        │  - HTTPS termination             │
        │  - Request routing               │
        │  - Rate limiting                 │
        └────────────┬──────────────────────┘
                     │
        ┌────────────▼─────────────────────────────┐
        │     Load Balancer                        │
        │  - Distributes traffic to app nodes     │
        │  - Health checks                         │
        │  - Session affinity (if needed)          │
        └────────┬──────────────────────────────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
┌───▼──┐    ┌───▼──┐    ┌───▼──┐
│App 1 │    │App 2 │ ... │App N │  (Stateless Node.js services)
│Node  │    │Node  │    │Node  │
└───┬──┘    └───┬──┘    └───┬──┘
    │           │           │
    └───────────┼───────────┘
                │
        ┌───────▼────────┐
        │ Connection Pool│
        │  (Max 20 conn) │
        └───────┬────────┘
                │
        ┌───────▼────────────────────┐
        │  PostgreSQL Database       │
        │  (Primary + Read Replicas) │
        │  - ACID transactions       │
        │  - Backups & PITR          │
        └────────────────────────────┘
```

---

## Environment Tiers

### Development Environment
**Purpose:** Local development with minimal setup

**Technology Stack:**
- SQLite (file-based, zero-config)
- Node.js + Express (local development server)
- React dev server (Vite with HMR)
- Docker Compose (optional containerization)

**Configuration:**
```yaml
database: sqlite
debug: true
logging: console
cache: memory
authentication: jwt (no expiry for dev)
```

**Setup:**
```bash
npm install
npm run dev  # Starts both frontend and backend
```

---

### Test Environment
**Purpose:** Automated testing with isolated data

**Technology Stack:**
- PostgreSQL (in Docker)
- Node.js + Express
- Jest test runner
- Ephemeral database (reset per test suite)

**Configuration:**
```yaml
database: postgresql (test container)
debug: true
logging: file
cache: memory
seed_data: test fixtures
authentication: jwt (short expiry for tests)
```

**Isolation:**
- Separate database per test suite
- Auto-cleanup after test completion
- Deterministic test data

---

### Production Environment
**Purpose:** High-availability, scalable deployment

**Technology Stack:**
- PostgreSQL (managed RDS or self-hosted with HA)
- Node.js + Express (containerized)
- Redis (cache cluster)
- Kubernetes or managed container service
- Nginx reverse proxy
- CloudFront or similar CDN

**Configuration:**
```yaml
database: postgresql (HA with replication)
debug: false
logging: structured (JSON, centralized)
cache: redis (cluster)
authentication: jwt (24-hour expiry)
ssl: tls 1.2+
backup: hourly snapshots
monitoring: prometheus + grafana
```

---

## Containerization

### Docker Image

**Base Image:** node:18-alpine (minimal, secure)

**Dockerfile Strategy:**
```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Runtime stage
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./
EXPOSE 5000
CMD ["node", "dist/main.js"]
```

**Image Size:** < 200MB

**Registry:** Docker Hub, ECR, or private registry

---

## Deployment Strategy

### Blue-Green Deployment
```
Current Production (Blue)
  └─ Running v1.0
     └─ Serving 100% traffic
        └─ Health: OK
           └─ Monitoring: Active

New Deployment (Green)
  └─ Staged v1.1
     └─ Serving 0% traffic initially
        └─ Health checks: Running
           └─ Smoke tests: Executing
              └─ Pass: Switch traffic
              └─ Fail: Rollback to Blue
```

**Benefits:**
- Zero-downtime deployments
- Fast rollback capability
- A/B testing ready
- Canary release support

**Process:**
1. Deploy new version to Green environment
2. Run smoke tests and health checks
3. Switch load balancer routing (0-10% traffic initially)
4. Monitor metrics (error rate, latency, etc.)
5. Gradually increase traffic (10% → 25% → 50% → 100%)
6. Keep Blue running for 24 hours (immediate rollback option)
7. Decommission Blue environment

---

## Database Deployment

### Schema Migrations
```
Database Version: v1.0
  ├─ 001_init_schema.sql (users, tasks, teams, etc.)
  ├─ 002_audit_log.sql (audit table)
  ├─ 003_indexes.sql (performance indexes)
  └─ 004_seed_data.sql (reference data)

Deployment Process:
  1. Backup current database
  2. Run pending migrations in order
  3. Validate schema changes
  4. Smoke test critical queries
  5. Monitor for issues during 24-hour window
  6. If issue detected: Restore from backup, fix, redeploy
```

**Rollback Strategy:**
- Backward-compatible migrations (add columns, don't remove)
- Dual-write period during migration
- Rollback scripts for each migration

---

## Configuration Management

### Environment Variables
```bash
# Database
DB_HOST=postgres.example.com
DB_PORT=5432
DB_NAME=taskdb
DB_USER=appuser
DB_PASSWORD=${SECRET}

# JWT
JWT_SECRET=${SECRET}
JWT_EXPIRY=86400  # 24 hours

# Server
NODE_ENV=production
PORT=5000
LOG_LEVEL=info

# Cache
REDIS_HOST=redis.example.com
REDIS_PORT=6379

# Monitoring
SENTRY_DSN=${SECRET}
PROMETHEUS_PORT=9090

# Email (future)
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=${SECRET}
SMTP_PASSWORD=${SECRET}
```

### Secrets Management
- **Tool:** AWS Secrets Manager, HashiCorp Vault, or Azure Key Vault
- **Rotation:** Annual minimum
- **Access:** Only application service accounts
- **Audit:** All accesses logged

---

## Infrastructure as Code (IaC)

### Terraform/CloudFormation Structure
```
infra/
├── vpc.tf                   # VPC, subnets, security groups
├── database.tf              # RDS PostgreSQL
├── cache.tf                 # Redis cluster
├── kubernetes.tf            # EKS/GKE cluster
├── networking.tf            # ALB, NLB, DNS
├── monitoring.tf            # CloudWatch/Prometheus
├── secrets.tf               # Secrets management
└── variables.tf             # Environment configuration
```

---

## Monitoring & Observability

### Metrics Collection

**Application Metrics:**
- API response time (p50, p95, p99)
- Request throughput (requests/second)
- Error rate (5xx, 4xx)
- Authentication success/failure
- Task operation latency
- Search query performance

**Infrastructure Metrics:**
- CPU usage per pod
- Memory usage per pod
- Database connection pool
- Database query latency
- Cache hit rate
- Network I/O

**Business Metrics:**
- Tasks created per day
- Task completion rate
- User signups
- Concurrent users

### Monitoring Tools
- **Prometheus:** Metrics collection
- **Grafana:** Visualization dashboards
- **Sentry:** Error tracking and alerts
- **CloudWatch/ELK:** Log aggregation

### Alerting
```yaml
Alerts:
  - CPU > 80% → Warn (scale up if persistent)
  - API latency p95 > 2s → Alert (investigate)
  - Error rate > 1% → Critical alert (page on-call)
  - Database connections > 15/20 → Warn (connection leak)
  - Disk space < 10% → Critical (prevent out-of-space)
```

---

## Backup & Disaster Recovery

### Backup Strategy
- **Frequency:** Hourly snapshots (production)
- **Retention:** 30-day rolling window
- **Storage:** Separate region/account
- **Encryption:** At-rest encryption on backups
- **Verification:** Weekly restore test

### Recovery Objectives
- **RTO (Recovery Time Objective):** 1 hour (point-in-time restore)
- **RPO (Recovery Point Objective):** 15 minutes (hourly backups)

### Disaster Recovery Procedure
1. Detect failure (monitoring alerts)
2. Activate DR plan (failover to standby)
3. Notify stakeholders
4. Restore from backup (if needed)
5. Verify data integrity
6. Route traffic to recovered infrastructure
7. Post-incident review

---

## Scaling Strategy

### Horizontal Scaling
```
Low Traffic (off-peak)
  ├─ 1-2 app nodes
  └─ RDS single instance

Normal Traffic (peak)
  ├─ 3-5 app nodes
  └─ RDS multi-AZ

High Demand (spike)
  ├─ 5-10 app nodes
  └─ RDS read replicas
```

**Auto-Scaling Policy:**
- Scale up when CPU > 70% or traffic increases
- Scale down when CPU < 30% for 10+ minutes
- Min replicas: 2 (high availability)
- Max replicas: 10 (cost control)

### Vertical Scaling
- Database: Increase instance type (CPU, memory, storage)
- Cache: Scale Redis cluster horizontally
- Load balancer: Increase capacity if needed

---

## Security in Deployment

### Network Security
- **VPC:** Private subnets for database and cache
- **Security Groups:** Ingress rules restrict access
- **WAF:** Application firewall blocks common attacks
- **DDoS Protection:** CloudFront or similar service

### Access Control
- **SSH Keys:** Managed via secrets, never in code
- **IAM Roles:** Services assume roles with minimal permissions
- **Audit Logging:** All access logged and monitored

### Secrets Handling
- **No secrets in code:** Injected via environment
- **No secrets in logs:** Masked before logging
- **Rotation:** Automated key rotation

---

## Health Checks

### Liveness Probe
```
GET /health/live
Response: 200 OK if application is running
Frequency: Every 10 seconds
Failure threshold: 3 consecutive failures → restart
```

### Readiness Probe
```
GET /health/ready
Checks:
  - Database connectivity
  - Cache availability
  - Dependent services
Response: 200 OK if ready to serve traffic
Frequency: Every 5 seconds
Failure: Remove from load balancer until ready
```

---

## Performance Optimization

### Frontend
- **Code Splitting:** Lazy load routes, components
- **Minification:** Production builds minified
- **Asset Compression:** Gzip/brotli compression
- **Caching:** Browser cache headers (Cache-Control)

### Backend
- **Connection Pooling:** PostgreSQL connection pool (max 20)
- **Query Optimization:** Indexes on frequently queried columns
- **Caching:** Redis for dashboard metrics (5-min TTL)
- **Rate Limiting:** Prevent abuse, ensure fair access

### Database
- **Indexes:** B-tree on owner, assignee, status, due_date
- **Full-Text Indexes:** Title + description search
- **Partitioning:** Partition large audit table by year (future)
- **Archival:** Move old audit records to cold storage

---

## CI/CD Pipeline

### Build Stage
```
Trigger: Push to main branch
  ├─ Run linter (ESLint)
  ├─ Run type checker (TypeScript)
  ├─ Run unit tests
  ├─ Build Docker image
  └─ Push to registry
```

### Deploy Stage
```
Manual approval required for production

Staging:
  ├─ Deploy to staging environment
  ├─ Run integration tests
  ├─ Run smoke tests
  └─ Manual QA approval

Production:
  ├─ Deploy using blue-green strategy
  ├─ Canary release (5% → 25% → 50% → 100%)
  ├─ Monitor metrics for 24 hours
  └─ Rollback trigger if error rate > 1%
```

---

## Support & Runbooks

### Common Operations
- **Database Backup:** `./scripts/backup.sh`
- **Scale Horizontally:** `kubectl scale deployment app --replicas=5`
- **View Logs:** `kubectl logs -f deployment/app`
- **Check Health:** `curl https://api.example.com/health/live`
- **Emergency Rollback:** `./scripts/rollback.sh v1.0`

### Contact & Escalation
- **On-Call:** PagerDuty
- **Critical Issues:** Slack #incidents
- **Database Team:** database-team@example.com
- **Infrastructure Team:** infra-team@example.com

---

## Document Control

- **Document ID:** DEPLOY-ARCH-001
- **Version:** 1.0
- **Author:** Solution Architect
- **Status:** Ready for DevOps Engineer Handoff
