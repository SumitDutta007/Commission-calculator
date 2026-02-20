/**
 * Custom hook for commission calculation.
 * 
 * Design Pattern: Custom React hook for state management
 * Benefits:
 * - Reusable logic
 * - Separation of concerns
 * - Type safety
 * - Loading/error states
 */
import { useState } from 'react';
import { 
  calculateCommission, 
  CommissionRequest, 
  CommissionResponse,
  ApiError 
} from '@/services/api';

interface UseCommissionCalculatorReturn {
  result: CommissionResponse | null;
  loading: boolean;
  error: string | null;
  calculate: (request: CommissionRequest) => Promise<void>;
  reset: () => void;
}

export function useCommissionCalculator(): UseCommissionCalculatorReturn {
  const [result, setResult] = useState<CommissionResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const calculate = async (request: CommissionRequest) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await calculateCommission(request);
      setResult(response);
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError.message || 'An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setResult(null);
    setError(null);
    setLoading(false);
  };

  return {
    result,
    loading,
    error,
    calculate,
    reset,
  };
}
