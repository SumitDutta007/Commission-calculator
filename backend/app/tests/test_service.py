"""
Test suite for Commission Calculator Service.

Testing Strategy:
- Boundary value analysis (79.99%, 80%, 80.01%)
- Equivalence partitioning
- Error path testing
- Large value testing
- Precision testing

Coverage Target: 100% of service layer
"""
import pytest
from decimal import Decimal

from app.services import CommissionCalculatorService, CommissionResult
from app.core.exceptions import ValidationError, BusinessRuleViolation


class TestCommissionCalculatorService:
    """Test suite for commission calculation logic."""
    
    @pytest.fixture
    def service(self) -> CommissionCalculatorService:
        """Provide a fresh service instance for each test."""
        return CommissionCalculatorService(
            commission_rate=0.05,
            eligibility_threshold=0.80
        )
    
    # ==============================================================
    # Boundary Value Testing - Critical Business Logic
    # ==============================================================
    
    def test_exactly_80_percent_of_target_is_eligible(self, service):
        """
        Test boundary condition: exactly 80% should be eligible.
        
        Business Rule: threshold is inclusive (>=)
        """
        sales = 96000.00
        target = 120000.00  # 96000 / 120000 = 0.80 = 80%
        
        result = service.calculate_commission(sales, target)
        
        assert result.eligible is True
        assert result.percentage_of_target == 80.00
        assert result.commission == 4800.00  # 5% of 96000
    
    def test_just_below_80_percent_is_not_eligible(self, service):
        """
        Test boundary condition: 79.99% should NOT be eligible.
        
        This is the critical edge case.
        Note: The actual value is 79.9999%, which rounds to 80.0% for display,
        but the precise comparison correctly determines ineligibility.
        """
        sales = 95999.99
        target = 120000.00  # 79.9999% of target
        
        result = service.calculate_commission(sales, target)
        
        # Key assertions: must be ineligible with zero commission
        assert result.eligible is False
        assert result.commission == 0.00
        # Displayed percentage rounds to 80.0%, but person is still ineligible
        assert result.percentage_of_target == 80.0
    
    def test_just_above_80_percent_is_eligible(self, service):
        """Test boundary condition: 80.01% should be eligible."""
        sales = 96012.00
        target = 120000.00  # 80.01% of target
        
        result = service.calculate_commission(sales, target)
        
        assert result.eligible is True
        assert result.percentage_of_target > 80.00
        assert result.commission > 0.00
    
    # ==============================================================
    # Example Test Cases from Requirements
    # ==============================================================
    
    def test_example_case_83_percent(self, service):
        """Test the primary example from requirements."""
        result = service.calculate_commission(
            sales_amount=100000.00,
            target_amount=120000.00
        )
        
        assert result.commission == 5000.00
        assert result.eligible is True
        assert result.percentage_of_target == 83.33
    
    def test_below_threshold_returns_zero_commission(self, service):
        """Test that ineligible sales get 0 commission."""
        result = service.calculate_commission(
            sales_amount=90000.00,  # 75% of target
            target_amount=120000.00
        )
        
        assert result.commission == 0.00
        assert result.eligible is False
        assert result.percentage_of_target == 75.00
    
    # ==============================================================
    # Edge Cases and Special Values
    # ==============================================================
    
    def test_zero_sales_returns_zero_commission(self, service):
        """Test zero sales amount."""
        result = service.calculate_commission(
            sales_amount=0.00,
            target_amount=120000.00
        )
        
        assert result.commission == 0.00
        assert result.eligible is False
        assert result.percentage_of_target == 0.00
    
    def test_sales_equal_to_target_is_eligible(self, service):
        """Test 100% target achievement."""
        result = service.calculate_commission(
            sales_amount=120000.00,
            target_amount=120000.00
        )
        
        assert result.commission == 6000.00  # 5% of 120000
        assert result.eligible is True
        assert result.percentage_of_target == 100.00
    
    def test_sales_exceed_target_is_eligible(self, service):
        """Test over-achievement (>100%)."""
        result = service.calculate_commission(
            sales_amount=150000.00,
            target_amount=120000.00
        )
        
        assert result.commission == 7500.00  # 5% of 150000
        assert result.eligible is True
        assert result.percentage_of_target == 125.00
    
    # ==============================================================
    # Large Value Testing (Overflow Protection)
    # ==============================================================
    
    def test_large_values_within_limit(self, service):
        """Test with large but valid amounts."""
        result = service.calculate_commission(
            sales_amount=999999999.00,  # ~1 billion
            target_amount=1000000000.00  # 1 billion
        )
        
        assert result.commission == 49999999.95  # 5% of 999999999
        assert result.eligible is True
        assert result.percentage_of_target == 100.00
    
    def test_very_small_values(self, service):
        """Test with small decimal values."""
        result = service.calculate_commission(
            sales_amount=0.80,
            target_amount=1.00
        )
        
        assert result.commission == 0.04  # 5% of 0.80
        assert result.eligible is True
        assert result.percentage_of_target == 80.00
    
    # ==============================================================
    # Decimal Precision Testing
    # ==============================================================
    
    def test_decimal_precision_is_maintained(self, service):
        """Test that calculations maintain 2 decimal places."""
        result = service.calculate_commission(
            sales_amount=100000.33,
            target_amount=120000.00
        )
        
        # Commission should be rounded to 2 decimals
        assert result.commission == 5000.02  # 5% of 100000.33
        assert isinstance(result.commission, float)
        
        # Percentage should be rounded to 2 decimals
        assert result.percentage_of_target == 83.33
    
    def test_repeating_decimal_is_rounded(self, service):
        """Test rounding of repeating decimals."""
        result = service.calculate_commission(
            sales_amount=100000.00,
            target_amount=120000.00
        )
        
        # 100000/120000 = 0.833333... should round to 83.33%
        assert result.percentage_of_target == 83.33
    
    # ==============================================================
    # Validation Testing
    # ==============================================================
    
    def test_negative_sales_raises_validation_error(self, service):
        """Test that negative sales amount is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            service.calculate_commission(
                sales_amount=-1000.00,
                target_amount=120000.00
            )
        
        assert "negative" in exc_info.value.message.lower()
    
    def test_zero_target_raises_validation_error(self, service):
        """Test that zero target is rejected (prevents division by zero)."""
        with pytest.raises(ValidationError) as exc_info:
            service.calculate_commission(
                sales_amount=100000.00,
                target_amount=0.00
            )
        
        assert "zero" in exc_info.value.message.lower()
    
    def test_negative_target_raises_validation_error(self, service):
        """Test that negative target is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            service.calculate_commission(
                sales_amount=100000.00,
                target_amount=-120000.00
            )
        
        assert exc_info.value.message is not None
    
    # ==============================================================
    # Configuration Testing
    # ==============================================================
    
    def test_custom_commission_rate(self):
        """Test service with custom commission rate."""
        service = CommissionCalculatorService(
            commission_rate=0.10,  # 10% instead of 5%
            eligibility_threshold=0.80
        )
        
        result = service.calculate_commission(
            sales_amount=100000.00,
            target_amount=120000.00
        )
        
        assert result.commission == 10000.00  # 10% of 100000
    
    def test_custom_threshold(self):
        """Test service with custom eligibility threshold."""
        service = CommissionCalculatorService(
            commission_rate=0.05,
            eligibility_threshold=0.90  # 90% instead of 80%
        )
        
        # 85% should NOT be eligible with 90% threshold
        result = service.calculate_commission(
            sales_amount=102000.00,  # 85% of 120000
            target_amount=120000.00
        )
        
        assert result.eligible is False
        assert result.commission == 0.00
    
    def test_invalid_commission_rate_raises_error(self):
        """Test that invalid commission rate is rejected."""
        with pytest.raises(BusinessRuleViolation):
            CommissionCalculatorService(
                commission_rate=1.5,  # > 100%
                eligibility_threshold=0.80
            )
    
    def test_invalid_threshold_raises_error(self):
        """Test that invalid threshold is rejected."""
        with pytest.raises(BusinessRuleViolation):
            CommissionCalculatorService(
                commission_rate=0.05,
                eligibility_threshold=1.5  # > 100%
            )
    
    # ==============================================================
    # Return Type Testing
    # ==============================================================
    
    def test_return_type_is_commission_result(self, service):
        """Test that return type is correct NamedTuple."""
        result = service.calculate_commission(
            sales_amount=100000.00,
            target_amount=120000.00
        )
        
        assert isinstance(result, tuple)
        assert hasattr(result, 'commission')
        assert hasattr(result, 'eligible')
        assert hasattr(result, 'percentage_of_target')
    
    def test_result_is_immutable(self, service):
        """Test that result cannot be modified (NamedTuple immutability)."""
        result = service.calculate_commission(
            sales_amount=100000.00,
            target_amount=120000.00
        )
        
        with pytest.raises(AttributeError):
            result.commission = 9999.00  # Should fail
