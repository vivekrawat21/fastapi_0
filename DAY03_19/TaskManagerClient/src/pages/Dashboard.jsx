import React, { useState, useCallback } from 'react'
import TaskForm from '../components/TaskForm'
import TaskList from '../components/TaskList'

const Dashboard = () => {
  const [user] = useState(() => {
    const storedUser = localStorage.getItem('user')
    return storedUser ? JSON.parse(storedUser) : null
  })
  const [refreshKey, setRefreshKey] = useState(0)

  const handleTaskCreated = useCallback(() => {
    setRefreshKey(prev => prev + 1)
  }, [])

  return (
    <div className="min-h-screen bg-linear-to-br from-slate-900 via-blue-900 to-indigo-900 pt-20">
      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h1 className="text-2xl sm:text-3xl font-bold text-white">
                Welcome back! 👋
              </h1>
              <p className="text-gray-400 mt-1">Here's what's on your plate today</p>
            </div>
            <div className="flex items-center gap-3">
              <div className="px-4 py-2 bg-white/5 backdrop-blur-sm rounded-xl border border-white/10">
                <span className="text-gray-400 text-sm">Today</span>
                <p className="text-white font-semibold">
                  {new Date().toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })}
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-6 lg:gap-8">

          <div className="lg:col-span-1">
            <TaskForm onTaskCreated={handleTaskCreated} />
          </div>

          <div className="lg:col-span-2">
            <TaskList key={refreshKey} />
          </div>
        </div>
      </main>
    </div>
  )
}

export default Dashboard
