/**
 * Tests for CommissionCalculator component.
 * 
 * Test Coverage:
 * - Rendering
 * - User interactions
 * - Form validation
 * - API integration
 * - Error handling
 * - Loading states
 */
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import CommissionCalculator from '@/components/CommissionCalculator';
import * as api from '@/services/api';

// Mock the API module
jest.mock('@/services/api');

describe('CommissionCalculator Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Rendering', () => {
    it('should render the form with all inputs', () => {
      render(<CommissionCalculator />);

      expect(screen.getByLabelText(/sales amount/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/target amount/i)).toBeInTheDocument();
      expect(
        screen.getByRole('button', { name: /calculate commission/i })
      ).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /reset/i })).toBeInTheDocument();
    });

    it('should display business rules information', () => {
      render(<CommissionCalculator />);

      expect(screen.getByText(/commission rules/i)).toBeInTheDocument();
      expect(screen.getByText(/minimum threshold: 80% of target/i)).toBeInTheDocument();
      expect(screen.getByText(/commission rate: 5% of sales amount/i)).toBeInTheDocument();
    });
  });

  describe('Form Validation', () => {
    it('should show error for negative sales amount', async () => {
      render(<CommissionCalculator />);
      const user = userEvent.setup();

      const salesInput = screen.getByLabelText(/sales amount/i);
      const targetInput = screen.getByLabelText(/target amount/i);
      const submitButton = screen.getByRole('button', {
        name: /calculate commission/i,
      });

      await user.type(salesInput, '-100');
      await user.type(targetInput, '1000');
      await user.click(submitButton);

      await waitFor(() => {
        expect(
          screen.getByText(/sales amount cannot be negative/i)
        ).toBeInTheDocument();
      });
    });

    it('should show error for zero target amount', async () => {
      render(<CommissionCalculator />);
      const user = userEvent.setup();

      const salesInput = screen.getByLabelText(/sales amount/i);
      const targetInput = screen.getByLabelText(/target amount/i);
      const submitButton = screen.getByRole('button', {
        name: /calculate commission/i,
      });

      await user.type(salesInput, '1000');
      await user.type(targetInput, '0');
      await user.click(submitButton);

      await waitFor(() => {
        expect(
          screen.getByText(/target amount must be greater than zero/i)
        ).toBeInTheDocument();
      });
    });

    it('should show error for amounts exceeding maximum', async () => {
      render(<CommissionCalculator />);
      const user = userEvent.setup();

      const salesInput = screen.getByLabelText(/sales amount/i);
      const targetInput = screen.getByLabelText(/target amount/i);
      const submitButton = screen.getByRole('button', {
        name: /calculate commission/i,
      });

      await user.type(salesInput, '9999999999999');
      await user.type(targetInput, '1000');
      await user.click(submitButton);

      await waitFor(() => {
        expect(
          screen.getByText(/amount too large/i)
        ).toBeInTheDocument();
      });
    });

    it('should show error for invalid input', async () => {
      render(<CommissionCalculator />);
      const user = userEvent.setup();

      const salesInput = screen.getByLabelText(/sales amount/i);
      const targetInput = screen.getByLabelText(/target amount/i);
      const submitButton = screen.getByRole('button', {
        name: /calculate commission/i,
      });

      await user.type(salesInput, 'abc');
      await user.type(targetInput, '1000');
      await user.click(submitButton);

      await waitFor(() => {
        expect(
          screen.getByText(/please enter valid numbers/i)
        ).toBeInTheDocument();
      });
    });
  });

  describe('API Integration', () => {
    it('should successfully calculate commission when eligible', async () => {
      const mockResponse = {
        commission: 5000,
        eligible: true,
        percentage_of_target: 83.33,
      };

      (api.calculateCommission as jest.Mock).mockResolvedValue(mockResponse);

      render(<CommissionCalculator />);
      const user = userEvent.setup();

      const salesInput = screen.getByLabelText(/sales amount/i);
      const targetInput = screen.getByLabelText(/target amount/i);
      const submitButton = screen.getByRole('button', {
        name: /calculate commission/i,
      });

      await user.type(salesInput, '100000');
      await user.type(targetInput, '120000');
      await user.click(submitButton);

      await waitFor(() => {
        expect(screen.getByText(/calculation results/i)).toBeInTheDocument();
      });

      expect(screen.getByText('$5,000.00')).toBeInTheDocument();
      expect(screen.getByText(/yes ✓/i)).toBeInTheDocument();
      expect(screen.getByText('83.33%')).toBeInTheDocument();
    });

    it('should successfully calculate commission when not eligible', async () => {
      const mockResponse = {
        commission: 0,
        eligible: false,
        percentage_of_target: 60.0,
      };

      (api.calculateCommission as jest.Mock).mockResolvedValue(mockResponse);

      render(<CommissionCalculator />);
      const user = userEvent.setup();

      const salesInput = screen.getByLabelText(/sales amount/i);
      const targetInput = screen.getByLabelText(/target amount/i);
      const submitButton = screen.getByRole('button', {
        name: /calculate commission/i,
      });

      await user.type(salesInput, '60000');
      await user.type(targetInput, '100000');
      await user.click(submitButton);

      await waitFor(() => {
        expect(screen.getByText(/calculation results/i)).toBeInTheDocument();
      });

      expect(screen.getByText('$0.00')).toBeInTheDocument();
      expect(screen.getByText(/no ✗/i)).toBeInTheDocument();
      expect(screen.getByText('60.00%')).toBeInTheDocument();
    });

    it('should display API error message', async () => {
      const mockError = {
        error: 'ValidationError',
        message: 'Invalid input provided',
        details: {},
      };

      (api.calculateCommission as jest.Mock).mockRejectedValue(mockError);

      render(<CommissionCalculator />);
      const user = userEvent.setup();

      const salesInput = screen.getByLabelText(/sales amount/i);
      const targetInput = screen.getByLabelText(/target amount/i);
      const submitButton = screen.getByRole('button', {
        name: /calculate commission/i,
      });

      await user.type(salesInput, '100000');
      await user.type(targetInput, '120000');
      await user.click(submitButton);

      await waitFor(() => {
        expect(screen.getByText(/invalid input provided/i)).toBeInTheDocument();
      });

      expect(screen.queryByText(/calculation results/i)).not.toBeInTheDocument();
    });
  });

  describe('Loading States', () => {
    it('should show loading state during API call', async () => {
      (api.calculateCommission as jest.Mock).mockImplementation(
        () => new Promise((resolve) => setTimeout(resolve, 1000))
      );

      render(<CommissionCalculator />);
      const user = userEvent.setup();

      const salesInput = screen.getByLabelText(/sales amount/i);
      const targetInput = screen.getByLabelText(/target amount/i);
      const submitButton = screen.getByRole('button', {
        name: /calculate commission/i,
      });

      await user.type(salesInput, '100000');
      await user.type(targetInput, '120000');
      await user.click(submitButton);

      expect(screen.getByText(/calculating\.\.\./i)).toBeInTheDocument();
      expect(submitButton).toBeDisabled();
    });

    it('should disable inputs during loading', async () => {
      (api.calculateCommission as jest.Mock).mockImplementation(
        () => new Promise((resolve) => setTimeout(resolve, 1000))
      );

      render(<CommissionCalculator />);
      const user = userEvent.setup();

      const salesInput = screen.getByLabelText(/sales amount/i);
      const targetInput = screen.getByLabelText(/target amount/i);
      const submitButton = screen.getByRole('button', {
        name: /calculate commission/i,
      });

      await user.type(salesInput, '100000');
      await user.type(targetInput, '120000');
      await user.click(submitButton);

      expect(salesInput).toBeDisabled();
      expect(targetInput).toBeDisabled();
    });
  });

  describe('Reset Functionality', () => {
    it('should clear form and results when reset is clicked', async () => {
      const mockResponse = {
        commission: 5000,
        eligible: true,
        percentage_of_target: 83.33,
      };

      (api.calculateCommission as jest.Mock).mockResolvedValue(mockResponse);

      render(<CommissionCalculator />);
      const user = userEvent.setup();

      const salesInput = screen.getByLabelText(/sales amount/i) as HTMLInputElement;
      const targetInput = screen.getByLabelText(/target amount/i) as HTMLInputElement;
      const submitButton = screen.getByRole('button', {
        name: /calculate commission/i,
      });
      const resetButton = screen.getByRole('button', { name: /reset/i });

      // Fill and submit
      await user.type(salesInput, '100000');
      await user.type(targetInput, '120000');
      await user.click(submitButton);

      await waitFor(() => {
        expect(screen.getByText(/calculation results/i)).toBeInTheDocument();
      });

      // Reset
      await user.click(resetButton);

      expect(salesInput.value).toBe('');
      expect(targetInput.value).toBe('');
      expect(screen.queryByText(/calculation results/i)).not.toBeInTheDocument();
    });
  });

  describe('Accessibility', () => {
    it('should have proper ARIA labels', () => {
      render(<CommissionCalculator />);

      expect(screen.getByLabelText(/sales amount/i)).toHaveAttribute(
        'aria-describedby',
        'sales-amount-help'
      );
      expect(screen.getByLabelText(/target amount/i)).toHaveAttribute(
        'aria-describedby',
        'target-amount-help'
      );
    });

    it('should have role="alert" for error messages', async () => {
      render(<CommissionCalculator />);
      const user = userEvent.setup();

      const salesInput = screen.getByLabelText(/sales amount/i);
      const targetInput = screen.getByLabelText(/target amount/i);
      const submitButton = screen.getByRole('button', {
        name: /calculate commission/i,
      });

      await user.type(salesInput, '-100');
      await user.type(targetInput, '1000');
      await user.click(submitButton);

      await waitFor(() => {
        const alert = screen.getByRole('alert');
        expect(alert).toBeInTheDocument();
      });
    });
  });
});
