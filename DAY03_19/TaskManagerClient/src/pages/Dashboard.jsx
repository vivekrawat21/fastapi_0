import React from 'react'
import { useSelector } from 'react-redux'
import { Link } from 'react-router-dom'
import TaskForm from '../components/TaskForm'
import TaskList from '../components/TaskList'

const Dashboard = () => {
  const { user } = useSelector((state) => state.auth)
  const isCollector = user?.role === 'COLLECTOR'

  return (
    <div className="min-h-screen bg-linear-to-br from-slate-900 via-blue-900 to-indigo-900 pt-20">
      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Upgrade Banner for Collectors */}
        {isCollector && (
          <div className="mb-6 p-4 bg-gradient-to-r from-yellow-500/20 to-orange-500/20 border border-yellow-500/30 rounded-xl flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-yellow-500/20 rounded-full flex items-center justify-center">
                <svg className="w-5 h-5 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <div>
                <p className="text-white font-medium">Upgrade to Pro</p>
                <p className="text-yellow-200/70 text-sm">Get access to delete tasks, admin features & more!</p>
              </div>
            </div>
            <Link
              to="/payment"
              className="px-4 py-2 bg-gradient-to-r from-yellow-500 to-orange-500 text-white font-medium rounded-lg hover:opacity-90 transition-opacity whitespace-nowrap"
            >
              Upgrade Now
            </Link>
          </div>
        )}

        {/* Welcome Section */}
        <div className="mb-8">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h1 className="text-2xl sm:text-3xl font-bold text-white">
                Welcome back{user?.name ? `, ${user.name}` : ''}! 👋
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
              {user?.role && (
                <div className={`px-3 py-1 rounded-full text-xs font-medium ${
                  user.role === 'ADMIN' 
                    ? 'bg-purple-500/20 text-purple-400 border border-purple-500/30' 
                    : user.role === 'SUPERVISOR' 
                    ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                    : 'bg-gray-500/20 text-gray-400 border border-gray-500/30'
                }`}>
                  {user.role}
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-6 lg:gap-8">

          <div className="lg:col-span-1">
            <TaskForm />
          </div>

          <div className="lg:col-span-2">
            <TaskList />
          </div>
        </div>
      </main>
    </div>
  )
}

export default Dashboard
