import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { tasksAPI } from '../../api/api'

// Async thunks
export const fetchTasks = createAsyncThunk(
  'tasks/fetchTasks',
  async (params = {}, { rejectWithValue }) => {
    try {
      const response = await tasksAPI.getAll(params)
      return response.data.items || response.data || []
    } catch (error) {
      const message = error.response?.data?.detail || 'Failed to fetch tasks'
      return rejectWithValue(message)
    }
  }
)

export const fetchTaskById = createAsyncThunk(
  'tasks/fetchTaskById',
  async (id, { rejectWithValue }) => {
    try {
      const response = await tasksAPI.getById(id)
      return response.data
    } catch (error) {
      const message = error.response?.data?.detail || 'Failed to fetch task'
      return rejectWithValue(message)
    }
  }
)

export const createTask = createAsyncThunk(
  'tasks/createTask',
  async (taskData, { rejectWithValue }) => {
    try {
      const response = await tasksAPI.create(taskData)
      return response.data
    } catch (error) {
      const message = error.response?.data?.detail || 'Failed to create task'
      return rejectWithValue(message)
    }
  }
)

export const updateTask = createAsyncThunk(
  'tasks/updateTask',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      const response = await tasksAPI.update(id, data)
      return response.data
    } catch (error) {
      const message = error.response?.data?.detail || 'Failed to update task'
      return rejectWithValue(message)
    }
  }
)

export const deleteTask = createAsyncThunk(
  'tasks/deleteTask',
  async (id, { rejectWithValue }) => {
    try {
      await tasksAPI.delete(id)
      return id
    } catch (error) {
      const message = error.response?.data?.detail || 'Failed to delete task'
      return rejectWithValue(message)
    }
  }
)

// Initial state
const initialState = {
  tasks: [],
  currentTask: null,
  filter: 'all',
  isLoading: false,
  isCreating: false,
  isUpdating: false,
  isDeleting: false,
  error: null,
  successMessage: null,
}

// Slice
const tasksSlice = createSlice({
  name: 'tasks',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null
    },
    clearSuccess: (state) => {
      state.successMessage = null
    },
    setFilter: (state, action) => {
      state.filter = action.payload
    },
    clearTasks: (state) => {
      state.tasks = []
      state.currentTask = null
      state.error = null
    },
    // Optimistic updates
    optimisticUpdateTask: (state, action) => {
      const { id, data } = action.payload
      const index = state.tasks.findIndex(task => task.id === id)
      if (index !== -1) {
        state.tasks[index] = { ...state.tasks[index], ...data }
      }
    },
    optimisticDeleteTask: (state, action) => {
      state.tasks = state.tasks.filter(task => task.id !== action.payload)
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch all tasks
      .addCase(fetchTasks.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(fetchTasks.fulfilled, (state, action) => {
        state.isLoading = false
        state.tasks = action.payload
      })
      .addCase(fetchTasks.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload
      })
      // Fetch single task
      .addCase(fetchTaskById.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(fetchTaskById.fulfilled, (state, action) => {
        state.isLoading = false
        state.currentTask = action.payload
      })
      .addCase(fetchTaskById.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload
      })
      // Create task
      .addCase(createTask.pending, (state) => {
        state.isCreating = true
        state.error = null
      })
      .addCase(createTask.fulfilled, (state, action) => {
        state.isCreating = false
        state.tasks.unshift(action.payload)
        state.successMessage = 'Task created successfully'
      })
      .addCase(createTask.rejected, (state, action) => {
        state.isCreating = false
        state.error = action.payload
      })
      // Update task
      .addCase(updateTask.pending, (state) => {
        state.isUpdating = true
        state.error = null
      })
      .addCase(updateTask.fulfilled, (state, action) => {
        state.isUpdating = false
        const index = state.tasks.findIndex(task => task.id === action.payload.id)
        if (index !== -1) {
          state.tasks[index] = action.payload
        }
        state.successMessage = 'Task updated successfully'
      })
      .addCase(updateTask.rejected, (state, action) => {
        state.isUpdating = false
        state.error = action.payload
      })
      // Delete task
      .addCase(deleteTask.pending, (state) => {
        state.isDeleting = true
        state.error = null
      })
      .addCase(deleteTask.fulfilled, (state, action) => {
        state.isDeleting = false
        state.tasks = state.tasks.filter(task => task.id !== action.payload)
        state.successMessage = 'Task deleted successfully'
      })
      .addCase(deleteTask.rejected, (state, action) => {
        state.isDeleting = false
        state.error = action.payload
      })
  },
})

// Selectors
export const selectTasks = (state) => state.tasks.tasks
export const selectCurrentTask = (state) => state.tasks.currentTask
export const selectTasksLoading = (state) => state.tasks.isLoading
export const selectTasksError = (state) => state.tasks.error
export const selectTasksFilter = (state) => state.tasks.filter
export const selectIsCreating = (state) => state.tasks.isCreating
export const selectIsUpdating = (state) => state.tasks.isUpdating
export const selectIsDeleting = (state) => state.tasks.isDeleting
export const selectSuccessMessage = (state) => state.tasks.successMessage

// Computed selectors
export const selectFilteredTasks = (state) => {
  const { tasks, filter } = state.tasks
  if (filter === 'all') return tasks
  return tasks.filter(task => task.status === filter)
}

export const selectTaskStats = (state) => {
  const tasks = state.tasks.tasks
  return {
    total: tasks.length,
    pending: tasks.filter(t => t.status === 'pending').length,
    inProgress: tasks.filter(t => t.status === 'in_progress').length,
    completed: tasks.filter(t => t.status === 'completed').length,
  }
}

export const { 
  clearError, 
  clearSuccess, 
  setFilter, 
  clearTasks,
  optimisticUpdateTask,
  optimisticDeleteTask,
} = tasksSlice.actions

export default tasksSlice.reducer
