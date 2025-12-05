import React, { useState, useEffect } from 'react'
import { useSelector } from 'react-redux'
import { usersAPI } from '../api/api'

const Admin = () => {
  const { user } = useSelector((state) => state.auth)
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [editingUser, setEditingUser] = useState(null)
  const [showDeleteModal, setShowDeleteModal] = useState(false)
  const [userToDelete, setUserToDelete] = useState(null)

  const isAdmin = user?.role?.toUpperCase() === 'ADMIN'

  useEffect(() => {
    fetchUsers()
  }, [])

  const fetchUsers = async () => {
    try {
      setLoading(true)
      const response = await usersAPI.getAll()
      setUsers(response.data.users || [])
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch users')
    } finally {
      setLoading(false)
    }
  }

  const handleUpdateUser = async (userId, updates) => {
    try {
      await usersAPI.update(userId, updates)
      await fetchUsers()
      setEditingUser(null)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update user')
    }
  }

  const handleDeleteUser = async (userId) => {
    try {
      await usersAPI.delete(userId)
      await fetchUsers()
      setShowDeleteModal(false)
      setUserToDelete(null)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to delete user')
    }
  }

  const getRoleBadgeColor = (role) => {
    switch (role?.toUpperCase()) {
      case 'ADMIN':
        return 'bg-red-500/20 text-red-400 border-red-500/30'
      case 'SUPERVISOR':
        return 'bg-purple-500/20 text-purple-400 border-purple-500/30'
      case 'COLLECTOR':
      default:
        return 'bg-blue-500/20 text-blue-400 border-blue-500/30'
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-500"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900 pt-20">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">
            {isAdmin ? 'Admin Dashboard' : 'User Management'}
          </h1>
          <p className="text-gray-400">
            {isAdmin 
              ? 'Manage users, roles, and permissions' 
              : 'View all users in the system'}
          </p>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-500/20 border border-red-500/30 rounded-xl text-red-400">
            {error}
            <button 
              onClick={() => setError(null)} 
              className="ml-4 text-red-300 hover:text-white"
            >
              ✕
            </button>
          </div>
        )}

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white/5 backdrop-blur-xl rounded-xl border border-white/10 p-4">
            <p className="text-gray-400 text-sm">Total Users</p>
            <p className="text-2xl font-bold text-white">{users.length}</p>
          </div>
          <div className="bg-white/5 backdrop-blur-xl rounded-xl border border-white/10 p-4">
            <p className="text-gray-400 text-sm">Admins</p>
            <p className="text-2xl font-bold text-red-400">
              {users.filter(u => u.role?.toUpperCase() === 'ADMIN').length}
            </p>
          </div>
          <div className="bg-white/5 backdrop-blur-xl rounded-xl border border-white/10 p-4">
            <p className="text-gray-400 text-sm">Supervisors</p>
            <p className="text-2xl font-bold text-purple-400">
              {users.filter(u => u.role?.toUpperCase() === 'SUPERVISOR').length}
            </p>
          </div>
          <div className="bg-white/5 backdrop-blur-xl rounded-xl border border-white/10 p-4">
            <p className="text-gray-400 text-sm">Collectors</p>
            <p className="text-2xl font-bold text-blue-400">
              {users.filter(u => u.role?.toUpperCase() === 'COLLECTOR').length}
            </p>
          </div>
        </div>

        {/* Users Table */}
        <div className="bg-white/5 backdrop-blur-xl rounded-2xl border border-white/10 overflow-hidden">
          <div className="p-6 border-b border-white/10">
            <h2 className="text-xl font-bold text-white">All Users</h2>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-white/5">
                <tr>
                  <th className="px-6 py-4 text-left text-sm font-medium text-gray-400">ID</th>
                  <th className="px-6 py-4 text-left text-sm font-medium text-gray-400">Name</th>
                  <th className="px-6 py-4 text-left text-sm font-medium text-gray-400">Email</th>
                  <th className="px-6 py-4 text-left text-sm font-medium text-gray-400">Role</th>
                  <th className="px-6 py-4 text-left text-sm font-medium text-gray-400">Status</th>
                  {isAdmin && (
                    <th className="px-6 py-4 text-left text-sm font-medium text-gray-400">Actions</th>
                  )}
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {users.map((u) => (
                  <tr key={u.id} className="hover:bg-white/5 transition">
                    <td className="px-6 py-4 text-gray-300">#{u.id}</td>
                    <td className="px-6 py-4">
                      {editingUser?.id === u.id ? (
                        <input
                          type="text"
                          value={editingUser.name}
                          onChange={(e) => setEditingUser({ ...editingUser, name: e.target.value })}
                          className="bg-white/10 border border-white/20 rounded px-2 py-1 text-white"
                        />
                      ) : (
                        <span className="text-white font-medium">{u.name}</span>
                      )}
                    </td>
                    <td className="px-6 py-4">
                      {editingUser?.id === u.id ? (
                        <input
                          type="email"
                          value={editingUser.email}
                          onChange={(e) => setEditingUser({ ...editingUser, email: e.target.value })}
                          className="bg-white/10 border border-white/20 rounded px-2 py-1 text-white"
                        />
                      ) : (
                        <span className="text-gray-300">{u.email}</span>
                      )}
                    </td>
                    <td className="px-6 py-4">
                      {editingUser?.id === u.id && isAdmin ? (
                        <select
                          value={editingUser.role}
                          onChange={(e) => setEditingUser({ ...editingUser, role: e.target.value })}
                          className="bg-white/10 border border-white/20 rounded px-2 py-1 text-white"
                        >
                          <option value="COLLECTOR">Collector</option>
                          <option value="SUPERVISOR">Supervisor</option>
                          <option value="ADMIN">Admin</option>
                        </select>
                      ) : (
                        <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getRoleBadgeColor(u.role)}`}>
                          {u.role}
                        </span>
                      )}
                    </td>
                    <td className="px-6 py-4">
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                        u.is_active 
                          ? 'bg-green-500/20 text-green-400 border border-green-500/30' 
                          : 'bg-gray-500/20 text-gray-400 border border-gray-500/30'
                      }`}>
                        {u.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    {isAdmin && (
                      <td className="px-6 py-4">
                        <div className="flex gap-2">
                          {editingUser?.id === u.id ? (
                            <>
                              <button
                                onClick={() => handleUpdateUser(u.id, {
                                  name: editingUser.name,
                                  email: editingUser.email,
                                  role: editingUser.role
                                })}
                                className="px-3 py-1 bg-green-500/20 text-green-400 rounded-lg hover:bg-green-500/30 transition"
                              >
                                Save
                              </button>
                              <button
                                onClick={() => setEditingUser(null)}
                                className="px-3 py-1 bg-gray-500/20 text-gray-400 rounded-lg hover:bg-gray-500/30 transition"
                              >
                                Cancel
                              </button>
                            </>
                          ) : (
                            <>
                              <button
                                onClick={() => setEditingUser({ ...u })}
                                className="px-3 py-1 bg-blue-500/20 text-blue-400 rounded-lg hover:bg-blue-500/30 transition"
                              >
                                Edit
                              </button>
                              <button
                                onClick={() => {
                                  setUserToDelete(u)
                                  setShowDeleteModal(true)
                                }}
                                disabled={u.id === user?.id}
                                className="px-3 py-1 bg-red-500/20 text-red-400 rounded-lg hover:bg-red-500/30 transition disabled:opacity-50 disabled:cursor-not-allowed"
                              >
                                Delete
                              </button>
                            </>
                          )}
                        </div>
                      </td>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Role Permissions Info */}
        <div className="mt-8 bg-white/5 backdrop-blur-xl rounded-2xl border border-white/10 p-6">
          <h3 className="text-lg font-bold text-white mb-4">Role Permissions</h3>
          <div className="grid md:grid-cols-3 gap-4">
            <div className="p-4 bg-red-500/10 rounded-xl border border-red-500/20">
              <h4 className="font-semibold text-red-400 mb-2">Admin</h4>
              <ul className="text-sm text-gray-400 space-y-1">
                <li>✓ View all users</li>
                <li>✓ Create/Edit/Delete users</li>
                <li>✓ Change user roles</li>
                <li>✓ Delete any task</li>
                <li>✓ Full system access</li>
              </ul>
            </div>
            <div className="p-4 bg-purple-500/10 rounded-xl border border-purple-500/20">
              <h4 className="font-semibold text-purple-400 mb-2">Supervisor (Pro Plan)</h4>
              <ul className="text-sm text-gray-400 space-y-1">
                <li>✓ View all users</li>
                <li>✓ Delete any task</li>
                <li>✓ Unlimited tasks</li>
                <li>✓ Advanced analytics</li>
                <li>✗ Cannot manage users</li>
              </ul>
            </div>
            <div className="p-4 bg-blue-500/10 rounded-xl border border-blue-500/20">
              <h4 className="font-semibold text-blue-400 mb-2">Collector (Free)</h4>
              <ul className="text-sm text-gray-400 space-y-1">
                <li>✓ Create own tasks</li>
                <li>✓ View own tasks</li>
                <li>✓ Edit own tasks</li>
                <li>✗ Cannot delete tasks</li>
                <li>✗ Cannot view users</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Delete Confirmation Modal */}
      {showDeleteModal && userToDelete && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-slate-800 rounded-2xl p-6 max-w-md w-full mx-4 border border-white/10">
            <h3 className="text-xl font-bold text-white mb-4">Confirm Delete</h3>
            <p className="text-gray-400 mb-6">
              Are you sure you want to delete user <span className="text-white font-medium">{userToDelete.name}</span>? 
              This action cannot be undone.
            </p>
            <div className="flex gap-4">
              <button
                onClick={() => handleDeleteUser(userToDelete.id)}
                className="flex-1 py-2 bg-red-500 text-white rounded-xl hover:bg-red-600 transition"
              >
                Delete
              </button>
              <button
                onClick={() => {
                  setShowDeleteModal(false)
                  setUserToDelete(null)
                }}
                className="flex-1 py-2 bg-gray-600 text-white rounded-xl hover:bg-gray-700 transition"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Admin
