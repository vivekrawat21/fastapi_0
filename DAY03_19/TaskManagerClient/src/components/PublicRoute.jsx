import React from 'react'
import { Navigate } from 'react-router-dom'

const PublicRoute = ({ children }) => {
  const token = localStorage.getItem('access_token')
  const user = localStorage.getItem('user')

  if (token && user) {
    return <Navigate to="/" replace />
  }

  return children
}

export default PublicRoute