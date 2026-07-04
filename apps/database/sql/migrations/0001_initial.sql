-- 0001_initial.sql
-- Idempotent starter migration for Task Management System schema
BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS migration_history (
    migration_id TEXT PRIMARY KEY,
    applied_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    description TEXT NOT NULL
);

INSERT INTO migration_history(migration_id, description)
SELECT '0001_initial', 'Initial schema creation for Task Management System'
WHERE NOT EXISTS (SELECT 1 FROM migration_history WHERE migration_id = '0001_initial');

COMMIT;
