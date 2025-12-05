import React from 'react'
import { Link } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { setBillingCycle, processPayment } from '../store/slices/paymentSlice'

const Payment = () => {
  const dispatch = useDispatch()
  const { billingCycle, plans, currentPlan, isProcessing, error, successMessage } = useSelector((state) => state.payment)
  const { user } = useSelector((state) => state.auth)

  // Determine current plan based on user role
  const userRole = user?.role || 'COLLECTOR'
  const effectiveCurrentPlan = userRole === 'SUPERVISOR' ? 'pro' : userRole === 'ADMIN' ? 'enterprise' : 'free'

  const handleBillingCycleChange = (cycle) => {
    dispatch(setBillingCycle(cycle))
  }

  const handleUpgrade = (planId) => {
    dispatch(processPayment({ planId, billingCycle }))
  }

  // Map plans to display format based on user role
  const displayPlans = plans.map(plan => {
    const isCurrentPlan = plan.id === effectiveCurrentPlan
    let cta = 'Upgrade'
    if (plan.id === 'free') {
      cta = isCurrentPlan ? 'Current Plan' : 'Free Plan'
    } else if (plan.id === 'pro') {
      cta = isCurrentPlan ? 'Current Plan' : 'Upgrade to Pro'
    } else {
      cta = isCurrentPlan ? 'Current Plan' : 'Contact Sales'
    }
    
    return {
      ...plan,
      cta,
      highlighted: plan.id === 'pro',
      disabled: isCurrentPlan || plan.id === 'enterprise',
    }
  })

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900 py-24">
      {/* Background decorations */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-500/20 rounded-full blur-3xl"></div>
        <div className="absolute top-1/2 -left-40 w-80 h-80 bg-purple-500/20 rounded-full blur-3xl"></div>
      </div>

      <div className="relative container mx-auto px-4 sm:px-6 lg:px-8">
        {/* Error/Success Messages */}
        {error && (
          <div className="max-w-2xl mx-auto mb-6 p-4 bg-red-500/20 border border-red-500/30 rounded-xl text-red-400 text-center">
            {error}
          </div>
        )}
        {successMessage && (
          <div className="max-w-2xl mx-auto mb-6 p-4 bg-green-500/20 border border-green-500/30 rounded-xl text-green-400 text-center">
            {successMessage}
          </div>
        )}

        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-white/10 backdrop-blur-sm rounded-full border border-white/20 mb-6">
            <span className="w-2 h-2 bg-yellow-400 rounded-full animate-pulse"></span>
            <span className="text-gray-300 text-sm font-medium">Special Launch Offer - 20% Off</span>
          </div>
          <h1 className="text-4xl sm:text-5xl font-extrabold text-white mb-4">
            Choose Your Plan
          </h1>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Unlock powerful features and take your productivity to the next level
          </p>

          {/* Billing Toggle */}
          <div className="mt-8 inline-flex items-center gap-4 bg-white/10 p-1.5 rounded-xl">
            <button
              onClick={() => handleBillingCycleChange('monthly')}
              className={`px-6 py-2.5 rounded-lg font-medium transition-all ${
                billingCycle === 'monthly'
                  ? 'bg-white text-slate-900'
                  : 'text-gray-300 hover:text-white'
              }`}
            >
              Monthly
            </button>
            <button
              onClick={() => handleBillingCycleChange('yearly')}
              className={`px-6 py-2.5 rounded-lg font-medium transition-all flex items-center gap-2 ${
                billingCycle === 'yearly'
                  ? 'bg-white text-slate-900'
                  : 'text-gray-300 hover:text-white'
              }`}
            >
              Yearly
              <span className="text-xs bg-green-500 text-white px-2 py-0.5 rounded-full">Save 17%</span>
            </button>
          </div>
        </div>

        {/* Pricing Cards */}
        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {displayPlans.map((plan) => (
            <div
              key={plan.name}
              className={`relative p-8 rounded-2xl border backdrop-blur-xl transition-all ${
                plan.highlighted
                  ? 'bg-gradient-to-b from-blue-500/20 to-purple-500/20 border-blue-500/50 shadow-2xl shadow-blue-500/20 scale-105'
                  : 'bg-white/5 border-white/10 hover:border-white/20'
              }`}
            >
              {plan.highlighted && (
                <div className="absolute -top-4 left-1/2 -translate-x-1/2">
                  <span className="bg-gradient-to-r from-blue-500 to-purple-500 text-white text-sm font-semibold px-4 py-1.5 rounded-full">
                    Most Popular
                  </span>
                </div>
              )}

              <div className="mb-6">
                <h3 className="text-2xl font-bold text-white mb-2">{plan.name}</h3>
                <p className="text-gray-400">{plan.description}</p>
              </div>

              <div className="mb-6">
                <div className="flex items-baseline gap-1">
                  <span className="text-4xl font-extrabold text-white">
                    ₹{plan.price[billingCycle]}
                  </span>
                  {plan.price[billingCycle] > 0 && (
                    <span className="text-gray-400">/{billingCycle === 'monthly' ? 'mo' : 'yr'}</span>
                  )}
                </div>
                {plan.price[billingCycle] === 0 && (
                  <span className="text-gray-400">Forever free</span>
                )}
              </div>

              <button
                onClick={() => !plan.disabled && handleUpgrade(plan.id)}
                disabled={plan.disabled || isProcessing}
                className={`w-full py-3.5 rounded-xl font-semibold transition-all mb-8 ${
                  plan.disabled
                    ? 'bg-white/10 text-gray-400 cursor-not-allowed'
                    : plan.highlighted
                    ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white hover:opacity-90 shadow-lg shadow-blue-500/30'
                    : 'bg-white text-slate-900 hover:bg-gray-100'
                }`}
              >
                {plan.cta}
              </button>

              <div className="space-y-4">
                <p className="text-sm font-semibold text-white">What's included:</p>
                <ul className="space-y-3">
                  {plan.features.map((feature) => (
                    <li key={feature} className="flex items-center gap-3 text-gray-300">
                      <svg className="w-5 h-5 text-green-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                      </svg>
                      {feature}
                    </li>
                  ))}
                  {plan.notIncluded.map((feature) => (
                    <li key={feature} className="flex items-center gap-3 text-gray-500">
                      <svg className="w-5 h-5 text-gray-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>

        {/* FAQ / Trust Section */}
        <div className="mt-20 text-center">
          <div className="flex flex-wrap justify-center gap-8 text-gray-400">
            <div className="flex items-center gap-2">
              <svg className="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
              <span>Secure Payment</span>
            </div>
            <div className="flex items-center gap-2">
              <svg className="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
              </svg>
              <span>Cancel Anytime</span>
            </div>
            <div className="flex items-center gap-2">
              <svg className="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              <span>30-Day Money Back</span>
            </div>
          </div>

          <p className="mt-8 text-gray-400">
            Have questions?{' '}
            <Link to="/dashboard" className="text-blue-400 hover:underline">
              Contact our support team
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}

export default Payment
