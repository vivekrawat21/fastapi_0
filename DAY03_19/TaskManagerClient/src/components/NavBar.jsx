import React from 'react'
import { Link } from 'react-router-dom'

const NavBar = () => {
  const user = localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')) : null

  const handleLogout = () => {
    localStorage.removeItem('user')
    window.location.reload()
  }

  return (
    <nav className="bg-blue-600 p-4">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-white text-xl font-bold">TaskManager</Link>
        <div>
          {user ? (
            <>
              <Link to="/dashboard" className="text-white mr-4">Dashboard</Link>
              <Link to="/tasks" className="text-white mr-4">Tasks</Link>
              <span className="text-white mr-4">Welcome {user.name}</span>
              <button onClick={handleLogout} className="text-white">Logout</button>
            </>
          ) : (
            <Link to="/login" className="text-white">Login</Link>
          )}
        </div>
      </div>
    </nav>
  )
}

export default NavBar