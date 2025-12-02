import React, { useState } from 'react'
import { tasksAPI } from '../api/api'

const TaskForm = ({ userId, onTaskCreated }) => {
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [priority, setPriority] = useState('medium')
  const [dueDate, setDueDate] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')
    setLoading(true)
    try {
      await tasksAPI.create({
        title,
        description,
        priority,
        status: 'pending',
        due_date: dueDate || new Date().toISOString().split('T')[0],
      })
      setTitle('')
      setDescription('')
      setPriority('medium')
      setDueDate('')
      setSuccess('Task created successfully!')
      if (onTaskCreated) onTaskCreated()
      setTimeout(() => setSuccess(''), 3000)
    } catch (error) {
      console.error('Error creating task:', error)
      setError(error.response?.data?.detail || 'Failed to create task. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const priorityColors = {
    low: 'bg-green-500/20 text-green-400 border-green-500/30',
    medium: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
    high: 'bg-red-500/20 text-red-400 border-red-500/30'
  }

  return (
    <div className="bg-white/5 backdrop-blur-xl rounded-2xl border border-white/10 p-6 sticky top-24">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 bg-gradient-to-r from-green-500 to-emerald-500 rounded-xl flex items-center justify-center">
          <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" />
          </svg>
        </div>
        <h2 className="text-xl font-bold text-white">Create New Task</h2>
      </div>

      {error && (
        <div className="bg-red-500/20 border border-red-500/30 text-red-400 p-3 rounded-xl mb-4 text-sm">
          {error}
        </div>
      )}
      
      {success && (
        <div className="bg-green-500/20 border border-green-500/30 text-green-400 p-3 rounded-xl mb-4 text-sm">
          {success}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-gray-300 font-medium mb-1">Title *</label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            placeholder="What needs to be done?"
            required
          />
        </div>

        <div>
          <label className="block text-gray-300 font-medium mb-1">Description</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all resize-none"
            rows="3"
            placeholder="Add more details..."
          />
        </div>

        <div>
          <label className="block text-gray-300 font-medium mb-2">Priority</label>
          <div className="flex gap-2">
            {['low', 'medium', 'high'].map((p) => (
              <button
                key={p}
                type="button"
                onClick={() => setPriority(p)}
                className={`flex-1 py-2 px-3 rounded-xl border font-medium capitalize transition-all ${
                  priority === p
                    ? priorityColors[p]
                    : 'bg-white/5 text-gray-400 border-white/10 hover:bg-white/10'
                }`}
              >
                {p}
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-gray-300 font-medium mb-1">Due Date</label>
          <input
            type="date"
            value={dueDate}
            onChange={(e) => setDueDate(e.target.value)}
            className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-gradient-to-r from-blue-500 to-indigo-600 text-white py-3 rounded-xl font-semibold hover:from-blue-600 hover:to-indigo-700 transition-all disabled:opacity-50 flex items-center justify-center gap-2 shadow-lg shadow-blue-500/20"
        >
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              Creating...
            </>
          ) : (
            <>
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" />
              </svg>
              Create Task
            </>
          )}
        </button>
      </form>
    </div>
  )
}

export default TaskForm