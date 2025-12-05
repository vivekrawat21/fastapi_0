import React, { useEffect } from 'react'
import { Routes, Route } from 'react-router-dom'
import { useDispatch } from 'react-redux'
import { initializeAuth } from './store/slices/authSlice'
import Home from './pages/Home.jsx'
import Tasks from './pages/Tasks.jsx'
import Login from './pages/Login.jsx'
import Dashboard from './pages/Dashboard.jsx'
import Error from './pages/Error.jsx'
import NoLayout from './Layouts/NoLayout.jsx'
import MainLayout from './Layouts/MainLayout.jsx'
import Register from './pages/Register.jsx'
import PublicRoute from './components/PublicRoute.jsx'
import ProtectedRoute from './components/ProtectedRoute.jsx'
import RoleProtectedRoute from './components/RoleProtectedRoute.jsx'
import Payment from './pages/Payment.jsx'
import Admin from './pages/Admin.jsx'


const App = () => {
  const dispatch = useDispatch()

  useEffect(() => {
    dispatch(initializeAuth())
  }, [dispatch])

  return (
    <Routes>
      <Route element={<NoLayout />}>
        <Route path="/login" element={<PublicRoute><Login /></PublicRoute>} />
        <Route path='/register' element={<PublicRoute><Register /></PublicRoute>} />
        
        <Route path="*" element={<Error />} />
      </Route>

      <Route element={<MainLayout />}>
        <Route path='/payment' element={<Payment />} />
        <Route path="/" element={<Home />} />
        <Route path="/tasks" element={<ProtectedRoute><Tasks /></ProtectedRoute>} />
        <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
        <Route path="/admin" element={
          <RoleProtectedRoute allowedRoles={['ADMIN', 'SUPERVISOR']}>
            <Admin />
          </RoleProtectedRoute>
        } />
      </Route>
    </Routes>
  )
}

export default App