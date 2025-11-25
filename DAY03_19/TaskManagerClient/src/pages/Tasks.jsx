import React, { useEffect, useState } from 'react'
import TaskList from '../components/TaskList'

const Tasks = () => {
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
      <h1 className="text-3xl font-bold mb-6">All Tasks</h1>
      <TaskList userId={user.id} />
    </div>
  )
}

export default Tasks