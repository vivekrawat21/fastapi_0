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

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900 pt-20">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-2xl sm:text-3xl font-bold text-white">All Tasks</h1>
          <p className="text-gray-400 mt-1">View and manage all your tasks</p>
        </div>
        <TaskList userId={user?.id} />
      </div>
    </div>
  )
}

export default Tasks