import React from 'react'
import { useNavigate } from 'react-router-dom'

export default function Register(){
  const nav = useNavigate()
  function handleSubmit(e: React.FormEvent){
    e.preventDefault()
    nav('/dashboard')
  }
  return (
    <section>
      <h1>Create Account</h1>
      <form onSubmit={handleSubmit} aria-label="register form">
        <label>Full name<input name="name" required/></label>
        <label>Email<input name="email" type="email" required/></label>
        <label>Password<input name="password" type="password" required/></label>
        <button type="submit" className="btn-primary">Create Account</button>
      </form>
    </section>
  )
}
