import React from 'react'

export default function Dashboard(){
  return (
    <section>
      <div className="hero-gradient" aria-hidden="true"></div>
      <div style={{display:'flex',gap:16,alignItems:'center',marginBottom:16}}>
        <div className="avatar-initials" aria-hidden>JW</div>
        <div>
          <div style={{fontWeight:700}}>Product Lead · Product</div>
          <div className="muted">San Francisco, CA · Joined March 2023</div>
        </div>
      </div>

      <h2>Overview</h2>
      <p>Summary cards and recent activity will appear here.</p>
    </section>
  )
}

