import React, { useEffect, useState } from 'react'
import TaskForm from '../components/TaskForm'
import TaskList from '../components/TaskList'

const Dashboard = () => {
  const [user, setUser] = useState(null)

  useEffect(() => {
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      setUser(JSON.parse(storedUser))
    }
  }, [])

  if (!user) return <div>Please login first</div>

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">Dashboard - Welcome {user.name}</h1>
      <TaskForm userId={user.id} onTaskCreated={() => window.location.reload()} />
      <TaskList userId={user.id} />
    </div>
  )
}

export default Dashboard