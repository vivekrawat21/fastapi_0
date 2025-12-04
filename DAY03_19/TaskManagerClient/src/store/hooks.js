// Custom hooks for Redux store
import { useDispatch, useSelector } from 'react-redux'

// Typed hooks for better TypeScript support in future
export const useAppDispatch = () => useDispatch()
export const useAppSelector = useSelector

// Auth hooks
export { 
  selectAuth,
  selectUser,
  selectIsAuthenticated,
  selectAuthLoading,
  selectAuthError,
  selectIsInitialized,
} from './slices/authSlice'

// Tasks hooks
export {
  selectTasks,
  selectCurrentTask,
  selectTasksLoading,
  selectTasksError,
  selectTasksFilter,
  selectFilteredTasks,
  selectTaskStats,
  selectIsCreating,
  selectIsUpdating,
  selectIsDeleting,
  selectSuccessMessage,
} from './slices/tasksSlice'

// Payment hooks
export {
  selectPlans,
  selectCurrentPlan,
  selectSubscription,
  selectBillingCycle,
  selectIsProcessing,
  selectPaymentError,
  selectPaymentSuccess,
  selectCurrentPlanDetails,
  selectIsPremium,
} from './slices/paymentSlice'
