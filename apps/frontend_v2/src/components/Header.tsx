import React from 'react'
import { Link } from 'react-router-dom'

export default function Header(){
  return (
    <header className="app-header">
      <div className="header-inner">
        <Link to="/dashboard" className="brand">Specs Frontend</Link>
        <nav>
          <Link to="/tasks">Tasks</Link>
          <Link to="/profile">Profile</Link>
          <Link to="/settings">Settings</Link>
        </nav>
      </div>
    </header>
  )
}
