-- Seed data for local development/testing.

INSERT INTO users (id, name, email, password_hash, role)
VALUES
    ('11111111-1111-1111-1111-111111111111', 'Admin User', 'admin@example.com', '$2b$12$examplehashadmin', 'admin'),
    ('22222222-2222-2222-2222-222222222222', 'Team Lead', 'lead@example.com', '$2b$12$examplehashlead', 'teamlead'),
    ('33333333-3333-3333-3333-333333333333', 'Member User', 'member@example.com', '$2b$12$examplehashmember', 'member')
ON CONFLICT (email) DO NOTHING;

INSERT INTO tasks (
    id,
    title,
    description,
    due_date,
    priority,
    status,
    creator_id,
    assignee_id,
    created_at,
    updated_at
)
VALUES
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
        'Setup repository quality gates',
        'Configure linting, formatting, and test pipeline.',
        CURRENT_DATE + INTERVAL '7 days',
        'high',
        'in_progress',
        '11111111-1111-1111-1111-111111111111',
        '22222222-2222-2222-2222-222222222222',
        NOW(),
        NOW()
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
        'Draft onboarding tasks',
        'Create first-week onboarding tasks for new members.',
        CURRENT_DATE + INTERVAL '14 days',
        'medium',
        'todo',
        '22222222-2222-2222-2222-222222222222',
        '33333333-3333-3333-3333-333333333333',
        NOW(),
        NOW()
    )
ON CONFLICT (id) DO NOTHING;

INSERT INTO notifications (id, recipient_id, task_id, type, message)
VALUES
    (
        'cccccccc-cccc-cccc-cccc-cccccccccccc',
        '33333333-3333-3333-3333-333333333333',
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
        'assignment',
        'You were assigned task Draft onboarding tasks.'
    )
ON CONFLICT (id) DO NOTHING;
