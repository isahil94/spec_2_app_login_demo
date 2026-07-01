CREATE OR REPLACE FUNCTION fn_can_transition_task_status(
    p_current task_status,
    p_next task_status
)
RETURNS BOOLEAN
LANGUAGE sql
IMMUTABLE
AS $$
    SELECT CASE
        WHEN p_current = 'todo' AND p_next = 'in_progress' THEN TRUE
        WHEN p_current = 'in_progress' AND p_next IN ('todo', 'in_review') THEN TRUE
        WHEN p_current = 'in_review' AND p_next IN ('in_progress', 'done') THEN TRUE
        ELSE FALSE
    END;
$$;
