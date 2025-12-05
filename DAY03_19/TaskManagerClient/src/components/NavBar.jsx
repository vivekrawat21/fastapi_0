import React, { useState } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { logout, selectUser, selectIsAuthenticated } from '../store/slices/authSlice'

const NavBar = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const location = useLocation()
  
  const user = useSelector(selectUser)
  const isAuthenticated = useSelector(selectIsAuthenticated)

  const handleLogout = () => {
    dispatch(logout())
    navigate('/')
  }

  const isActive = (path) => location.pathname === path

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 backdrop-blur-xl bg-slate-900/80 border-b border-white/10">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-indigo-500 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/20">
              <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
              </svg>
            </div>
            <span className="text-xl font-bold text-white">
              TaskManager
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-6">
            {isAuthenticated ? (
              <>
                <Link
                  to="/"
                  className={`font-medium transition-colors px-4 py-2 rounded-lg ${
                    isActive('/') 
                      ? 'text-blue-400 bg-blue-500/10' 
                      : 'text-gray-300 hover:text-white hover:bg-white/10'
                  }`}
                >
                  Home
                </Link>
                <Link
                  to="/dashboard"
                  className={`font-medium transition-colors px-4 py-2 rounded-lg ${
                    isActive('/dashboard') 
                      ? 'text-blue-400 bg-blue-500/10' 
                      : 'text-gray-300 hover:text-white hover:bg-white/10'
                  }`}
                >
                  Dashboard
                </Link>
                <Link
                  to="/tasks"
                  className={`font-medium transition-colors px-4 py-2 rounded-lg ${
                    isActive('/tasks') 
                      ? 'text-blue-400 bg-blue-500/10' 
                      : 'text-gray-300 hover:text-white hover:bg-white/10'
                  }`}
                >
                  Tasks
                </Link>
                <Link
                  to="/payment"
                  className={`font-medium transition-colors px-4 py-2 rounded-lg ${
                    isActive('/payment')
                      ? 'text-yellow-400 bg-yellow-500/10'
                      : 'text-gray-300 hover:text-white hover:bg-white/10'
                  }`}
                >
                  Pricing
                </Link>
                {/* Admin link - only for Admin and Supervisor */}
                {(user?.role?.toUpperCase() === 'ADMIN' || user?.role?.toUpperCase() === 'SUPERVISOR') && (
                  <Link
                    to="/admin"
                    className={`font-medium transition-colors px-4 py-2 rounded-lg ${
                      isActive('/admin')
                        ? 'text-purple-400 bg-purple-500/10'
                        : 'text-gray-300 hover:text-white hover:bg-white/10'
                    }`}
                  >
                    {user?.role?.toUpperCase() === 'ADMIN' ? 'Admin' : 'Users'}
                  </Link>
                )}
                <div className="flex items-center gap-3 pl-4 border-l border-white/10">
                  <div className="w-9 h-9 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center">
                    <span className="text-white font-semibold text-sm">
                      {user?.name?.charAt(0).toUpperCase() || user?.email?.charAt(0).toUpperCase()}
                    </span>
                  </div>
                  <div className="flex flex-col">
                    <span className="text-gray-300 font-medium text-sm">{user?.name || user?.email}</span>
                    <span className={`text-xs ${
                      user?.role?.toUpperCase() === 'ADMIN' ? 'text-red-400' :
                      user?.role?.toUpperCase() === 'SUPERVISOR' ? 'text-purple-400' : 'text-blue-400'
                    }`}>
                      {user?.role}
                    </span>
                  </div>
                  <button
                    onClick={handleLogout}
                    className="ml-2 px-4 py-2 text-red-400 hover:bg-red-500/10 rounded-lg transition-colors font-medium"
                  >
                    Logout
                  </button>
                </div>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="text-gray-300 font-medium hover:text-white transition-colors px-4 py-2 rounded-lg hover:bg-white/10"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="bg-gradient-to-r from-blue-500 to-indigo-500 text-white px-6 py-2.5 rounded-xl font-medium hover:from-blue-600 hover:to-indigo-600 transition-all shadow-lg shadow-blue-500/20"
                >
                  Sign Up
                </Link>
              </>
            )}
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              {mobileMenuOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <div className="md:hidden py-4 border-t border-white/10">
            {isAuthenticated ? (
              <div className="space-y-2">
                <Link
                  to="/"
                  className="block px-4 py-3 text-gray-300 hover:text-white hover:bg-white/10 rounded-xl transition-colors"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Home
                </Link>
                <Link
                  to="/dashboard"
                  className="block px-4 py-3 text-gray-300 hover:text-white hover:bg-white/10 rounded-xl transition-colors"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Dashboard
                </Link>
                <Link
                  to="/tasks"
                  className="block px-4 py-3 text-gray-300 hover:text-white hover:bg-white/10 rounded-xl transition-colors"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Tasks
                </Link>
                <Link
                  to="/payment"
                  className="block px-4 py-3 text-gray-300 hover:text-white hover:bg-white/10 rounded-xl transition-colors"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Pricing
                </Link>
                <div className="border-t border-white/10 pt-3 mt-3">
                  <div className="px-4 py-2 text-gray-500 text-sm">Signed in as {user.name || user.email}</div>
                  <button
                    onClick={handleLogout}
                    className="w-full text-left px-4 py-3 text-red-400 hover:bg-red-500/10 rounded-xl transition-colors"
                  >
                    Logout
                  </button>
                </div>
              </div>
            ) : (
              <div className="space-y-2">
                <Link
                  to="/login"
                  className="block px-4 py-3 text-gray-300 hover:text-white hover:bg-white/10 rounded-xl transition-colors"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="block px-4 py-3 bg-gradient-to-r from-blue-500 to-indigo-500 text-white rounded-xl text-center font-medium"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Sign Up
                </Link>
              </div>
            )}
          </div>
        )}
      </div>
    </nav>
  )
}

export default NavBar