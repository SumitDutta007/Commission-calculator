/**
 * Tests for API service.
 */
import { calculateCommission, checkHealth } from '@/services/api';

global.fetch = jest.fn();

describe('API Service', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('calculateCommission', () => {
    it('should return commission response on success', async () => {
      const mockResponse = {
        commission: 5000,
        eligible: true,
        percentage_of_target: 83.33,
      };

      (global.fetch as jest.Mock).mockResolvedValue({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await calculateCommission({
        sales_amount: 100000,
        target_amount: 120000,
      });

      expect(result).toEqual(mockResponse);
      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/commission',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            sales_amount: 100000,
            target_amount: 120000,
          }),
        }
      );
    });

    it('should throw ApiError when API returns error', async () => {
      const mockErrorResponse = {
        error: 'ValidationError',
        message: 'Invalid input provided',
        details: { field: 'sales_amount' },
      };

      (global.fetch as jest.Mock).mockResolvedValue({
        ok: false,
        json: async () => mockErrorResponse,
      });

      await expect(
        calculateCommission({
          sales_amount: -100,
          target_amount: 1000,
        })
      ).rejects.toEqual({
        error: 'ValidationError',
        message: 'Invalid input provided',
        details: { field: 'sales_amount' },
      });
    });

    it('should throw network error when fetch fails', async () => {
      (global.fetch as jest.Mock).mockRejectedValue(
        new Error('Network error')
      );

      await expect(
        calculateCommission({
          sales_amount: 100000,
          target_amount: 120000,
        })
      ).rejects.toThrow('Network error. Please check your connection.');
    });
  });

  describe('checkHealth', () => {
    it('should return health status', async () => {
      const mockResponse = { status: 'healthy' };

      (global.fetch as jest.Mock).mockResolvedValue({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await checkHealth();

      expect(result).toEqual(mockResponse);
      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/v1/commission/health'
      );
    });
  });
});
