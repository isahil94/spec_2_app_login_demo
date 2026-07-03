import React from 'react'
import { useParams, Link } from 'react-router-dom'

export default function TaskDetails(){
  const { id } = useParams()
  return (
    <section>
      <h1>Task Details</h1>
      <p>Task id: {id}</p>
      <Link to={`/tasks/${id}/edit`} className="btn">Edit</Link>
    </section>
  )
}
