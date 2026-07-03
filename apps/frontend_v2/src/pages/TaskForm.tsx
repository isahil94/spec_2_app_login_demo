import React from 'react'
import { useNavigate } from 'react-router-dom'

export default function TaskForm({ edit }: { edit?: boolean }){
  const nav = useNavigate()
  function handleSubmit(e: React.FormEvent){
    e.preventDefault()
    nav('/tasks')
  }
  return (
    <section>
      <h1>{edit ? 'Edit Task' : 'Create Task'}</h1>
      <form onSubmit={handleSubmit} aria-label="task form">
        <label>Title<input name="title" required/></label>
        <label>Description<textarea name="description"/></label>
        <label>Priority<select name="priority"><option>Low</option><option>Medium</option><option>High</option></select></label>
        <button type="submit" className="btn-primary">Save</button>
      </form>
    </section>
  )
}
