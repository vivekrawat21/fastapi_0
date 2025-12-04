import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { authAPI } from '../../api/api'

// Async thunks
export const login = createAsyncThunk(
  'auth/login',
  async ({ email, password }, { rejectWithValue }) => {
    try {
      const response = await authAPI.login(email, password)
      const { access_token } = response.data
      
      // Store token in localStorage
      localStorage.setItem('access_token', access_token)
      
      // Decode token to get user info (basic decode, not verification)
      const payload = JSON.parse(atob(access_token.split('.')[1]))
      const user = {
        email: payload.sub,
        role: payload.role,
      }
      localStorage.setItem('user', JSON.stringify(user))
      
      return { user, token: access_token }
    } catch (error) {
      const message = error.response?.data?.detail || 'Login failed'
      return rejectWithValue(message)
    }
  }
)

export const register = createAsyncThunk(
  'auth/register',
  async ({ name, email, password, role = 'COLLECTOR' }, { rejectWithValue }) => {
    try {
      const response = await authAPI.register(name, email, password, role)
      return response.data
    } catch (error) {
      const message = error.response?.data?.detail || 'Registration failed'
      return rejectWithValue(message)
    }
  }
)

export const logout = createAsyncThunk(
  'auth/logout',
  async (_, { dispatch }) => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
    // Clear other slices
    dispatch({ type: 'tasks/clearTasks' })
    dispatch({ type: 'payment/clearPayment' })
    return null
  }
)

export const initializeAuth = createAsyncThunk(
  'auth/initialize',
  async (_, { rejectWithValue }) => {
    try {
      const token = localStorage.getItem('access_token')
      const userStr = localStorage.getItem('user')
      
      if (token && userStr) {
        const user = JSON.parse(userStr)
        return { user, token }
      }
      return null
    } catch (error) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')
      return rejectWithValue('Failed to initialize auth')
    }
  }
)

// Initial state
const initialState = {
  user: null,
  token: null,
  isAuthenticated: false,
  isLoading: false,
  isInitialized: false,
  error: null,
  registerSuccess: false,
}

// Slice
const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null
    },
    clearRegisterSuccess: (state) => {
      state.registerSuccess = false
    },
    setCredentials: (state, action) => {
      state.user = action.payload.user
      state.token = action.payload.token
      state.isAuthenticated = true
    },
  },
  extraReducers: (builder) => {
    builder
      // Login
      .addCase(login.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(login.fulfilled, (state, action) => {
        state.isLoading = false
        state.user = action.payload.user
        state.token = action.payload.token
        state.isAuthenticated = true
        state.error = null
      })
      .addCase(login.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload
        state.isAuthenticated = false
      })
      // Register
      .addCase(register.pending, (state) => {
        state.isLoading = true
        state.error = null
        state.registerSuccess = false
      })
      .addCase(register.fulfilled, (state) => {
        state.isLoading = false
        state.registerSuccess = true
        state.error = null
      })
      .addCase(register.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload
        state.registerSuccess = false
      })
      // Logout
      .addCase(logout.fulfilled, (state) => {
        state.user = null
        state.token = null
        state.isAuthenticated = false
        state.error = null
      })
      // Initialize
      .addCase(initializeAuth.pending, (state) => {
        state.isLoading = true
      })
      .addCase(initializeAuth.fulfilled, (state, action) => {
        state.isLoading = false
        state.isInitialized = true
        if (action.payload) {
          state.user = action.payload.user
          state.token = action.payload.token
          state.isAuthenticated = true
        }
      })
      .addCase(initializeAuth.rejected, (state) => {
        state.isLoading = false
        state.isInitialized = true
        state.isAuthenticated = false
      })
  },
})

// Selectors
export const selectAuth = (state) => state.auth
export const selectUser = (state) => state.auth.user
export const selectIsAuthenticated = (state) => state.auth.isAuthenticated
export const selectAuthLoading = (state) => state.auth.isLoading
export const selectAuthError = (state) => state.auth.error
export const selectIsInitialized = (state) => state.auth.isInitialized

export const { clearError, clearRegisterSuccess, setCredentials } = authSlice.actions
export default authSlice.reducer
