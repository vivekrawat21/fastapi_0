import React from 'react'
import { useSelector } from 'react-redux'
import TaskList from '../components/TaskList'
import { selectUser } from '../store/slices/authSlice'

const Tasks = () => {
  const user = useSelector(selectUser)

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900 pt-20">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-2xl sm:text-3xl font-bold text-white">All Tasks</h1>
          <p className="text-gray-400 mt-1">View and manage all your tasks</p>
        </div>
        <TaskList />
      </div>
    </div>
  )
}

export default Tasks