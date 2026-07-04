# Database Handoff Contract

## Metadata
- Version: 1.0
- Author: Database Developer
- Date: 2026-07-04
- Status: Draft
- Workflow ID: WF-20260704-001
- Artifact ID: DB-HANDOFF-001

## Stage
- Current Stage: Database Developer
- Consumed Inputs: artifacts/architecture/database-strategy.md, artifacts/architecture/data-dictionary.md, artifacts/architecture/api-specifications.md, artifacts/architecture/architecture-design.md, artifacts/requirements/data_requirements.md, artifacts/requirements/business_process_flows.md, artifacts/requirements/screen_elements.md
- Produced Outputs: apps/database/orm/models.py, apps/database/sql/schema.sql, apps/database/sql/migrations/0001_initial.sql, apps/database/sql/seed/sample_seed.sql, apps/database/init_db.py, artifacts/database/quality-report.md, artifacts/database/handoff-contract.md, artifacts/database/openlog.md

## Decisions and Rationale
- Implemented normalized schema for users, teams, tasks, comments, attachments, notifications, preferences, and audit entries.
- Enforced business rules for task lifecycle using enums, audit fields, soft-delete markers, and optimistic concurrency column `version`.
- Added separate `task_labels` table for normalized label storage and search indexing.
- Added `notification_preferences` so user notification event preference flags can be stored per user.
- Chose SQLite-compatible DDL for local development while preserving production compatibility through SQLAlchemy ORM and PostgreSQL-ready schema patterns.

## Assumptions
- Soft-delete and audit retention are managed at the application layer; current schema supports archived timestamp, not hard deletion.
- File attachments are metadata-only references; actual binary storage integration is deferred to a later implementation.
- `created_by` and `updated_by` fields are mandatory on top-level entities and are populated by business services.
- Default locale and theme values are seeded for new users; profile setting fields are nullable to support partial updates.

## Risks and Blockers
- Attachment file storage strategy is not defined in current artifacts; metadata-only implementation may require later migration.
- SQLite `PRAGMA foreign_keys` must be enabled in runtime connections to enforce FK constraints locally.
- `sql/migrations/0001_initial.sql` contains only migration history creation rather than full schema migration; full migration system must be integrated by backend migration tooling.

## Open Question Summary
- OQ-001: Need confirmation whether task labels should be stored as separate rows (`task_labels`) or as JSON array in tasks.
- OQ-002: Need confirmation on notification expiry and retention enforcement semantics for production.

## Next Agent Contract
- Next Agent: qa-engineer
- Required Events: DatabaseCompleted
- Expected Inputs: finalized backend repository pattern, API contract conformance checks, UI test scenarios
- Expected Outputs: database validation tests, query performance check, integration test cases, data integrity verification

## Validation Checklist
- [x] Schema tables defined
- [x] Keys and indexes defined
- [x] ORM models created
- [x] Seed data provided
- [x] Validation utility implemented
- [x] Persistent DB initialization path implemented
- [ ] Production migration integration pending
