/**
 * Commission Calculator Form Component - Sales Website Design
 * 
 * Modern, professional sales-focused UI with:
 * - Gradient backgrounds
 * - Animated elements
 * - Professional sales aesthetics
 * - Enhanced user experience
 */
'use client';

import { useState, FormEvent } from 'react';
import { useCommissionCalculator } from '@/hooks/useCommissionCalculator';

export default function CommissionCalculator() {
  const [salesAmount, setSalesAmount] = useState<string>('');
  const [targetAmount, setTargetAmount] = useState<string>('');
  const [validationError, setValidationError] = useState<string>('');

  const { result, loading, error, calculate, reset } = useCommissionCalculator();

  const validateInputs = (): boolean => {
    const sales = parseFloat(salesAmount);
    const target = parseFloat(targetAmount);

    if (salesAmount === '' || targetAmount === '') {
      setValidationError('Please enter valid numbers');
      return false;
    }

    if (isNaN(sales) || isNaN(target)) {
      setValidationError('Please enter valid numbers');
      return false;
    }

    if (sales < 0) {
      setValidationError('Sales amount cannot be negative');
      return false;
    }

    if (target <= 0) {
      setValidationError('Target amount must be greater than zero');
      return false;
    }

    if (sales > 1e12 || target > 1e12) {
      setValidationError('Amount too large (max: 1 trillion)');
      return false;
    }

    setValidationError('');
    return true;
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    if (!validateInputs()) {
      return;
    }

    await calculate({
      sales_amount: parseFloat(salesAmount),
      target_amount: parseFloat(targetAmount),
    });
  };

  const handleReset = () => {
    setSalesAmount('');
    setTargetAmount('');
    setValidationError('');
    reset();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Hero Header */}
      <div className="bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 text-white py-20 px-6 shadow-2xl relative overflow-hidden">
        <div className="absolute inset-0 bg-black opacity-10"></div>
        <div className="absolute inset-0 bg-gradient-to-b from-transparent to-black/20"></div>
        
        <div className="max-w-6xl mx-auto text-center relative z-10">
          <h1 className="text-6xl font-extrabold mb-6 tracking-tight drop-shadow-lg">
            Sales Commission Calculator
          </h1>
          <p className="text-2xl text-blue-100 max-w-3xl mx-auto mb-8 leading-relaxed">
            Calculate your earnings instantly and maximize your sales performance
          </p>
          <div className="flex flex-wrap justify-center gap-4 text-sm">
            <div className="bg-white/20 backdrop-blur-md px-6 py-3 rounded-full border border-white/30 hover:bg-white/30 transition-all duration-300">
              <span className="font-bold mr-2">✓</span> Real-time Calculations
            </div>
            <div className="bg-white/20 backdrop-blur-md px-6 py-3 rounded-full border border-white/30 hover:bg-white/30 transition-all duration-300">
              <span className="font-bold mr-2">✓</span> Performance Tracking
            </div>
            <div className="bg-white/20 backdrop-blur-md px-6 py-3 rounded-full border border-white/30 hover:bg-white/30 transition-all duration-300">
              <span className="font-bold mr-2">✓</span> Instant Results
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 -mt-16 pb-20">
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Calculator Card */}
          <div className="lg:col-span-2 bg-white rounded-3xl shadow-2xl p-10 border border-gray-100 transform hover:shadow-3xl transition-all duration-300">
            <div className="flex items-center gap-4 mb-8 pb-6 border-b border-gray-200">
              <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl flex items-center justify-center text-white text-2xl font-bold shadow-lg">
                $
              </div>
              <div>
                <h2 className="text-3xl font-bold text-gray-900">
                  Calculate Commission
                </h2>
                <p className="text-gray-500 text-base mt-1">
                  Enter your sales figures to calculate earnings
                </p>
              </div>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Sales Amount Input */}
              <div className="group">
                <label
                  htmlFor="sales-amount"
                  className="block text-sm font-bold text-gray-700 mb-3 uppercase tracking-wide"
                >
                  Sales Amount ($)
                </label>
                <div className="relative">
                  <span className="absolute left-4 top-4 text-gray-400 text-xl font-bold">$</span>
                  <input
                    id="sales-amount"
                    type="number"
                    step="0.01"
                    min="0"
                    value={salesAmount}
                    onChange={(e) => setSalesAmount(e.target.value)}
                    placeholder="100,000.00"
                    className="w-full pl-12 pr-6 py-4 border-2 border-gray-300 rounded-xl focus:ring-4 focus:ring-blue-500/30 focus:border-blue-500 text-xl font-semibold transition-all duration-200 group-hover:border-blue-400"
                    aria-describedby="sales-amount-help"
                    disabled={loading}
                  />
                </div>
                <p id="sales-amount-help" className="mt-2 text-sm text-gray-500">
                  Your actual sales amount achieved
                </p>
              </div>

              {/* Target Amount Input */}
              <div className="group">
                <label
                  htmlFor="target-amount"
                  className="block text-sm font-bold text-gray-700 mb-3 uppercase tracking-wide"
                >
                  Target Amount ($)
                </label>
                <div className="relative">
                  <span className="absolute left-4 top-4 text-gray-400 text-xl font-bold">$</span>
                  <input
                    id="target-amount"
                    type="number"
                    step="0.01"
                    min="0.01"
                    value={targetAmount}
                    onChange={(e) => setTargetAmount(e.target.value)}
                    placeholder="120,000.00"
                    className="w-full pl-12 pr-6 py-4 border-2 border-gray-300 rounded-xl focus:ring-4 focus:ring-indigo-500/30 focus:border-indigo-500 text-xl font-semibold transition-all duration-200 group-hover:border-indigo-400"
                    aria-describedby="target-amount-help"
                    disabled={loading}
                  />
                </div>
                <p id="target-amount-help" className="mt-2 text-sm text-gray-500">
                  Your sales target to achieve
                </p>
              </div>

              {/* Validation Error */}
              {validationError && (
                <div
                  className="p-5 bg-red-50 border-l-4 border-red-500 text-red-700 rounded-lg shadow-md"
                  role="alert"
                >
                  <div>
                    <p className="font-semibold">Validation Error</p>
                    <p className="text-sm">{validationError}</p>
                  </div>
                </div>
              )}

              {/* API Error */}
              {error && (
                <div
                  className="p-5 bg-red-50 border-l-4 border-red-500 text-red-700 rounded-lg shadow-md"
                  role="alert"
                >
                  <div>
                    <p className="font-semibold">Error</p>
                    <p className="text-sm">{error}</p>
                  </div>
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex gap-4 pt-4">
                <button
                  type="submit"
                  disabled={loading}
                  className={`flex-1 py-4 px-8 rounded-xl font-bold text-lg text-white transition-all duration-300 transform hover:scale-105 shadow-lg ${
                    loading
                      ? 'bg-gray-400 cursor-not-allowed'
                      : 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 hover:shadow-2xl'
                  }`}
                  aria-label="Calculate commission"
                >
                  {loading ? (
                    <span className="flex items-center justify-center gap-3">
                      <svg
                        className="animate-spin h-6 w-6 text-white"
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                      >
                        <circle
                          className="opacity-25"
                          cx="12"
                          cy="12"
                          r="10"
                          stroke="currentColor"
                          strokeWidth="4"
                        ></circle>
                        <path
                          className="opacity-75"
                          fill="currentColor"
                          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                        ></path>
                      </svg>
                      Calculating...
                    </span>
                  ) : (
                    'Calculate Commission'
                  )}
                </button>

                <button
                  type="button"
                  onClick={handleReset}
                  className="px-8 py-4 border-2 border-gray-300 rounded-xl font-bold text-lg text-gray-700 hover:bg-gray-50 hover:border-gray-400 transition-all duration-200"
                  aria-label="Reset form"
                >
                  Reset
                </button>
              </div>
            </form>

            {/* Results Display */}
            {result && (
              <div className="mt-10 p-8 bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl border-2 border-green-200 shadow-xl">
                <div className="mb-6">
                  <h2 className="text-2xl font-bold text-gray-900">
                    Commission Results
                  </h2>
                </div>

                <div className="grid gap-4">
                  {/* Commission Amount */}
                  <div className="flex justify-between items-center p-6 bg-white rounded-xl shadow-md border border-green-100 hover:shadow-lg transition-shadow duration-200">
                    <span className="text-lg font-semibold text-gray-700">Commission Earned:</span>
                    <span className="text-4xl font-extrabold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
                      ${result.commission.toLocaleString('en-US', {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2,
                      })}
                    </span>
                  </div>

                  {/* Eligibility Status */}
                  <div className="flex justify-between items-center p-6 bg-white rounded-xl shadow-md border border-green-100 hover:shadow-lg transition-shadow duration-200">
                    <span className="text-lg font-semibold text-gray-700">Eligibility Status:</span>
                    <span
                      className={`px-6 py-3 rounded-full font-bold text-lg ${
                        result.eligible
                          ? 'bg-green-100 text-green-700 border-2 border-green-300'
                          : 'bg-red-100 text-red-700 border-2 border-red-300'
                      }`}
                    >
                      {result.eligible ? 'ELIGIBLE' : 'NOT ELIGIBLE'}
                    </span>
                  </div>

                  {/* Performance */}
                  <div className="flex justify-between items-center p-6 bg-white rounded-xl shadow-md border border-green-100 hover:shadow-lg transition-shadow duration-200">
                    <span className="text-lg font-semibold text-gray-700">Target Achievement:</span>
                    <div className="text-right">
                      <span className="text-3xl font-bold text-indigo-600">
                        {result.percentage_of_target.toFixed(2)}%
                      </span>
                      <div className="w-48 h-3 bg-gray-200 rounded-full mt-2 overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full transition-all duration-1000"
                          style={{ width: `${Math.min(result.percentage_of_target, 100)}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Success Message */}
                {result.eligible && (
                  <div className="mt-6 p-4 bg-gradient-to-r from-green-400 to-emerald-500 rounded-xl text-white text-center font-semibold shadow-lg">
                    Congratulations! You've exceeded the threshold and earned your commission.
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Info Sidebar */}
          <div className="lg:col-span-1 space-y-6">
            {/* Commission Rules Card */}
            <div className="bg-gradient-to-br from-blue-500 to-indigo-600 text-white rounded-3xl shadow-2xl p-8">
              <h3 className="text-2xl font-bold mb-6 text-center">
                Commission Rules
              </h3>
              <ul className="space-y-4 text-base">
                <li className="bg-white/10 backdrop-blur-sm p-4 rounded-xl">
                  <p className="font-bold mb-1">Minimum Threshold</p>
                  <p className="text-sm text-blue-100">Must reach 80% of target</p>
                </li>
                <li className="bg-white/10 backdrop-blur-sm p-4 rounded-xl">
                  <p className="font-bold mb-1">Commission Rate</p>
                  <p className="text-sm text-blue-100">5% of sales amount</p>
                </li>
                <li className="bg-white/10 backdrop-blur-sm p-4 rounded-xl">
                  <p className="font-bold mb-1">Below Threshold</p>
                  <p className="text-sm text-blue-100">No commission earned</p>
                </li>
              </ul>
            </div>

            {/* Quick Tips Card */}
            <div className="bg-white rounded-3xl shadow-xl p-8 border border-gray-100">
              <h3 className="text-xl font-bold mb-4 text-gray-900 text-center">
                Quick Tips
              </h3>
              <ul className="space-y-3 text-sm text-gray-600">
                <li className="flex items-start gap-2">
                  <span className="text-blue-500 font-bold mt-0.5">•</span>
                  <span>Accurate numbers get accurate results</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-blue-500 font-bold mt-0.5">•</span>
                  <span>Track your progress regularly</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-blue-500 font-bold mt-0.5">•</span>
                  <span>Aim for 80%+ target achievement</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-blue-500 font-bold mt-0.5">•</span>
                  <span>Every sale counts towards your goal</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="bg-gray-900 text-white py-8 mt-12">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <p className="text-gray-400">
            © 2024 Sales Commission Calculator. Built for sales professionals.
          </p>
        </div>
      </div>
    </div>
  );
}
