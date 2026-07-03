import React from 'react'
import { useNavigate } from 'react-router-dom'

export default function Login(){
  const nav = useNavigate()
  function handleSubmit(e: React.FormEvent){
    e.preventDefault()
    // stubbed auth
    nav('/dashboard')
  }
  return (
    <section>
      <h1>Sign In</h1>
      <form onSubmit={handleSubmit} aria-label="login form">
        <label>Email<input name="email" type="email" required /></label>
        <label>Password<input name="password" type="password" required /></label>
        <button type="submit" className="btn-primary">Sign In</button>
      </form>
    </section>
  )
}
