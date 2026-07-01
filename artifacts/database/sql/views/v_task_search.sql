CREATE OR REPLACE VIEW v_task_search AS
SELECT
    t.id,
    t.title,
    t.description,
    t.due_date,
    t.priority,
    t.status,
    t.creator_id,
    t.assignee_id,
    t.created_at,
    t.updated_at,
    u_creator.name AS creator_name,
    u_assignee.name AS assignee_name,
    to_tsvector('english', COALESCE(t.title, '') || ' ' || COALESCE(t.description, '')) AS search_vector
FROM tasks t
JOIN users u_creator ON u_creator.id = t.creator_id
LEFT JOIN users u_assignee ON u_assignee.id = t.assignee_id
WHERE t.deleted_at IS NULL;
