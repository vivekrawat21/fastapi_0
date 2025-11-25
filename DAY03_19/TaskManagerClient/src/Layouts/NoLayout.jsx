import React from 'react'
import { Outlet } from 'react-router-dom'

const NoLayout = () => {
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <Outlet />
    </div>
  )
}

export default NoLayout