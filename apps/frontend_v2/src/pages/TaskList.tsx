import React from 'react'
import { Link } from 'react-router-dom'

export default function TaskList(){
  // minimal static list for scaffold
  const tasks = [
    { id: '1', title: 'Design login screen', status: 'todo' },
    { id: '2', title: 'Implement API contract', status: 'in-progress' }
  ]
  return (
    <section>
      <h1>Tasks</h1>
      <Link to="/tasks/new" className="btn-primary">Create Task</Link>
      <ul>
        {tasks.map(t=> (
          <li key={t.id}><Link to={`/tasks/${t.id}`}>{t.title} — {t.status}</Link></li>
        ))}
      </ul>
    </section>
  )
}
