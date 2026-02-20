/**
 * API Service for commission calculation.
 * 
 * Design Decisions:
 * - Centralized API calls
 * - Type-safe interfaces
 * - Error handling with custom types
 * - Configurable base URL
 */

export interface CommissionRequest {
  sales_amount: number;
  target_amount: number;
}

export interface CommissionResponse {
  commission: number;
  eligible: boolean;
  percentage_of_target: number;
}

export interface ApiError {
  error: string;
  message: string;
  details?: Record<string, any>;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Calculate commission via API.
 * 
 * @throws {ApiError} When API returns error response
 * @throws {Error} For network errors
 */
export async function calculateCommission(
  request: CommissionRequest
): Promise<CommissionResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/commission`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    const data = await response.json();

    if (!response.ok) {
      // API returned error response
      throw {
        error: data.error || 'APIError',
        message: data.message || 'An error occurred',
        details: data.details,
      } as ApiError;
    }

    return data as CommissionResponse;
  } catch (error) {
    // Network error or JSON parse error
    if ((error as ApiError).error) {
      throw error;
    }
    
    throw new Error('Network error. Please check your connection.');
  }
}

/**
 * Health check endpoint.
 */
export async function checkHealth(): Promise<{ status: string }> {
  const response = await fetch(`${API_BASE_URL}/api/v1/commission/health`);
  return response.json();
}
