import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { authAPI } from '../../api/api'
import { updateUserRole } from './authSlice'

// Pricing plans data
const pricingPlans = [
  {
    id: 'free',
    name: 'Free',
    price: { monthly: 0, yearly: 0 },
    description: 'Perfect for getting started',
    features: [
      'Up to 10 tasks',
      'Basic task management',
      'Email support',
      '1 project',
    ],
    notIncluded: [
      'Priority support',
      'Advanced analytics',
      'Team collaboration',
      'API access',
      'Delete tasks',
    ],
  },
  {
    id: 'pro',
    name: 'Pro',
    price: { monthly: 499, yearly: 4999 },
    description: 'Best for professionals - Become a Supervisor',
    features: [
      'Unlimited tasks',
      'Advanced task management',
      'Priority support',
      'Unlimited projects',
      'Advanced analytics',
      'Delete any task',
      'View all users',
      'Export to PDF/CSV',
    ],
    notIncluded: [
      'User management',
      'API access',
    ],
    popular: true,
  },
  {
    id: 'enterprise',
    name: 'Enterprise',
    price: { monthly: 1999, yearly: 19999 },
    description: 'For teams and organizations',
    features: [
      'Everything in Pro',
      'Team collaboration',
      'API access',
      'SSO integration',
      'Dedicated support',
      'Custom integrations',
      'Admin dashboard',
      'Audit logs',
    ],
    notIncluded: [],
  },
]

// Async thunks - connects to backend
export const processPayment = createAsyncThunk(
  'payment/processPayment',
  async ({ planId, billingCycle }, { rejectWithValue, dispatch }) => {
    try {
      const plan = pricingPlans.find(p => p.id === planId)
      if (!plan) {
        throw new Error('Invalid plan')
      }
      
      // Call backend to upgrade user to SUPERVISOR
      const response = await authAPI.subscribe(planId)
      
      // Update user in localStorage with new role
      const userStr = localStorage.getItem('user')
      if (userStr) {
        const user = JSON.parse(userStr)
        user.role = 'SUPERVISOR'
        localStorage.setItem('user', JSON.stringify(user))
      }
      
      // Update Redux auth state
      dispatch(updateUserRole('SUPERVISOR'))
      
      return {
        planId,
        planName: plan.name,
        billingCycle,
        amount: plan.price[billingCycle],
        subscribedAt: new Date().toISOString(),
        newRole: response.data.new_role,
        message: response.data.message,
      }
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || error.message || 'Payment failed')
    }
  }
)

export const fetchSubscription = createAsyncThunk(
  'payment/fetchSubscription',
  async (_, { rejectWithValue }) => {
    try {
      // Mock API call - replace with real subscription API
      const savedSubscription = localStorage.getItem('subscription')
      if (savedSubscription) {
        return JSON.parse(savedSubscription)
      }
      return null
    } catch (error) {
      return rejectWithValue('Failed to fetch subscription')
    }
  }
)

export const cancelSubscription = createAsyncThunk(
  'payment/cancelSubscription',
  async (_, { rejectWithValue }) => {
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      localStorage.removeItem('subscription')
      return null
    } catch (error) {
      return rejectWithValue('Failed to cancel subscription')
    }
  }
)

// Initial state
const initialState = {
  plans: pricingPlans,
  currentPlan: 'free',
  subscription: null,
  billingCycle: 'monthly',
  isProcessing: false,
  isLoading: false,
  error: null,
  successMessage: null,
}

// Slice
const paymentSlice = createSlice({
  name: 'payment',
  initialState,
  reducers: {
    setBillingCycle: (state, action) => {
      state.billingCycle = action.payload
    },
    clearError: (state) => {
      state.error = null
    },
    clearSuccess: (state) => {
      state.successMessage = null
    },
    clearPayment: (state) => {
      state.subscription = null
      state.currentPlan = 'free'
      state.error = null
    },
  },
  extraReducers: (builder) => {
    builder
      // Process payment
      .addCase(processPayment.pending, (state) => {
        state.isProcessing = true
        state.error = null
      })
      .addCase(processPayment.fulfilled, (state, action) => {
        state.isProcessing = false
        state.subscription = action.payload
        state.currentPlan = action.payload.planId
        state.successMessage = `Successfully subscribed to ${action.payload.planName}!`
        // Save to localStorage
        localStorage.setItem('subscription', JSON.stringify(action.payload))
      })
      .addCase(processPayment.rejected, (state, action) => {
        state.isProcessing = false
        state.error = action.payload
      })
      // Fetch subscription
      .addCase(fetchSubscription.pending, (state) => {
        state.isLoading = true
      })
      .addCase(fetchSubscription.fulfilled, (state, action) => {
        state.isLoading = false
        if (action.payload) {
          state.subscription = action.payload
          state.currentPlan = action.payload.planId
        }
      })
      .addCase(fetchSubscription.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload
      })
      // Cancel subscription
      .addCase(cancelSubscription.pending, (state) => {
        state.isProcessing = true
      })
      .addCase(cancelSubscription.fulfilled, (state) => {
        state.isProcessing = false
        state.subscription = null
        state.currentPlan = 'free'
        state.successMessage = 'Subscription cancelled successfully'
      })
      .addCase(cancelSubscription.rejected, (state, action) => {
        state.isProcessing = false
        state.error = action.payload
      })
  },
})

// Selectors
export const selectPlans = (state) => state.payment.plans
export const selectCurrentPlan = (state) => state.payment.currentPlan
export const selectSubscription = (state) => state.payment.subscription
export const selectBillingCycle = (state) => state.payment.billingCycle
export const selectIsProcessing = (state) => state.payment.isProcessing
export const selectPaymentError = (state) => state.payment.error
export const selectPaymentSuccess = (state) => state.payment.successMessage

// Computed selectors
export const selectCurrentPlanDetails = (state) => {
  const { plans, currentPlan } = state.payment
  return plans.find(p => p.id === currentPlan) || plans[0]
}

export const selectIsPremium = (state) => {
  return state.payment.currentPlan !== 'free'
}

export const { 
  setBillingCycle, 
  clearError, 
  clearSuccess,
  clearPayment,
} = paymentSlice.actions

export default paymentSlice.reducer
