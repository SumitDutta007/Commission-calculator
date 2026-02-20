/**
 * Tests for useCommissionCalculator hook.
 */
import { renderHook, act, waitFor } from '@testing-library/react';
import { useCommissionCalculator } from '@/hooks/useCommissionCalculator';
import * as api from '@/services/api';

jest.mock('@/services/api');

describe('useCommissionCalculator Hook', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should initialize with correct default values', () => {
    const { result } = renderHook(() => useCommissionCalculator());

    expect(result.current.result).toBeNull();
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBeNull();
  });

  it('should handle successful API call', async () => {
    const mockResponse = {
      commission: 5000,
      eligible: true,
      percentage_of_target: 83.33,
    };

    (api.calculateCommission as jest.Mock).mockResolvedValue(mockResponse);

    const { result } = renderHook(() => useCommissionCalculator());

    await act(async () => {
      await result.current.calculate({
        sales_amount: 100000,
        target_amount: 120000,
      });
    });

    expect(result.current.result).toEqual(mockResponse);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBeNull();
  });

  it('should handle API error', async () => {
    const mockError = {
      error: 'ValidationError',
      message: 'Invalid input',
    };

    (api.calculateCommission as jest.Mock).mockRejectedValue(mockError);

    const { result } = renderHook(() => useCommissionCalculator());

    await act(async () => {
      await result.current.calculate({
        sales_amount: -100,
        target_amount: 1000,
      });
    });

    expect(result.current.result).toBeNull();
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBe('Invalid input');
  });

  it('should set loading state during API call', async () => {
    (api.calculateCommission as jest.Mock).mockImplementation(
      () => new Promise((resolve) => setTimeout(resolve, 100))
    );

    const { result } = renderHook(() => useCommissionCalculator());

    act(() => {
      result.current.calculate({
        sales_amount: 100000,
        target_amount: 120000,
      });
    });

    expect(result.current.loading).toBe(true);

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });
  });

  it('should reset state when reset is called', async () => {
    const mockResponse = {
      commission: 5000,
      eligible: true,
      percentage_of_target: 83.33,
    };

    (api.calculateCommission as jest.Mock).mockResolvedValue(mockResponse);

    const { result } = renderHook(() => useCommissionCalculator());

    await act(async () => {
      await result.current.calculate({
        sales_amount: 100000,
        target_amount: 120000,
      });
    });

    expect(result.current.result).toEqual(mockResponse);

    act(() => {
      result.current.reset();
    });

    expect(result.current.result).toBeNull();
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBeNull();
  });
});
