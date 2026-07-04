# Task Management Database

This module contains the data layer implementation for the Task Management System, including schema definition, migrations, seed data, and initialization utilities.

## Contents

- `orm/models.py` — SQLAlchemy ORM model definitions for users, teams, tasks, comments, attachments, notifications, preferences, and audit entries.
- `sql/schema.sql` — canonical database schema DDL for SQLite/PostgreSQL compatibility.
- `sql/migrations/0001_initial.sql` — idempotent starter migration for schema creation.
- `sql/seed/sample_seed.sql` — sample data for initial environment validation.
- `init_db.py` — CLI utility to validate schema, initialize the persistent database, seed sample data, and verify the resulting database.

## Usage

From the repository root:

```powershell
python .\apps\database\init_db.py --validate
python .\apps\database\init_db.py --init --seed
python .\apps\database\init_db.py --verify
```

## Persistent Database Location

The SQLite persistent database is created at `apps/data/task_management.db`.

## Notes

- The schema is designed for SQLite development and PostgreSQL production.
- Audit entries are append-only by design.
- `NotificationPreference` is stored as a separate normalized table to support event preference settings.
