import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Header from './components/Header'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import TaskList from './pages/TaskList'
import TaskDetails from './pages/TaskDetails'
import TaskForm from './pages/TaskForm'
import Profile from './pages/Profile'
import Settings from './pages/Settings'

export default function App() {
  return (
    <div className="app-root">
      <Header />
      <main>
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/tasks" element={<TaskList />} />
          <Route path="/tasks/new" element={<TaskForm />} />
          <Route path="/tasks/:id" element={<TaskDetails />} />
          <Route path="/tasks/:id/edit" element={<TaskForm edit />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </main>
    </div>
  )
}
