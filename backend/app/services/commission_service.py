"""
Commission calculation service - Pure business logic.

Design Principles Applied:
- Single Responsibility: Only calculates commissions
- Dependency Inversion: Depends on abstractions (config), not concretions
- Open-Closed: New commission rules can extend without modifying core logic
- Testability: Pure functions, no external dependencies

This service is framework-agnostic and could be used in:
- FastAPI (current)
- Django
- AWS Lambda
- Background workers
"""
from typing import NamedTuple
from decimal import Decimal, ROUND_HALF_UP

from app.core.config import COMMISSION_RATE, ELIGIBILITY_THRESHOLD
from app.core.exceptions import ValidationError, BusinessRuleViolation


class CommissionResult(NamedTuple):
    """
    Immutable result object for commission calculation.
    
    Using NamedTuple for:
    - Immutability (thread-safe)
    - Clear structure
    - Type safety
    """
    commission: float
    eligible: bool
    percentage_of_target: float


class CommissionCalculatorService:
    """
    Service for calculating sales commissions.
    
    Stateless service following functional programming principles.
    All methods are pure functions (same input → same output).
    """
    
    def __init__(
        self,
        commission_rate: float = COMMISSION_RATE,
        eligibility_threshold: float = ELIGIBILITY_THRESHOLD
    ):
        """
        Initialize with configurable business rules.
        
        Args:
            commission_rate: Percentage of sales to award as commission
            eligibility_threshold: Minimum % of target required for eligibility
        
        Design Note: Dependency injection allows testing with different rules
        and supports multi-tenant scenarios with varying commission structures.
        """
        self._validate_configuration(commission_rate, eligibility_threshold)
        self.commission_rate = commission_rate
        self.eligibility_threshold = eligibility_threshold
    
    def calculate_commission(
        self,
        sales_amount: float,
        target_amount: float
    ) -> CommissionResult:
        """
        Calculate commission based on sales performance.
        
        Business Rules:
        1. Calculate percentage of target achieved
        2. If percentage < threshold → commission = 0
        3. If percentage >= threshold → commission = rate × sales_amount
        
        Args:
            sales_amount: Actual sales achieved
            target_amount: Sales target
        
        Returns:
            CommissionResult with commission, eligibility, and performance %
        
        Raises:
            ValidationError: If inputs violate business constraints
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        # Input validation
        self._validate_inputs(sales_amount, target_amount)
        
        # Calculate performance percentage (full precision for comparison)
        percentage_of_target_precise = self._calculate_percentage(
            sales_amount, target_amount
        )
        
        # Determine eligibility using precise value
        eligible = self._is_eligible(percentage_of_target_precise)
        
        # Calculate commission
        commission = self._calculate_commission_amount(
            sales_amount, eligible
        )
        
        # Round percentage for display (2 decimal places)
        percentage_for_display = round(percentage_of_target_precise, 2)
        
        return CommissionResult(
            commission=commission,
            eligible=eligible,
            percentage_of_target=percentage_for_display
        )
    
    def _validate_inputs(
        self,
        sales_amount: float,
        target_amount: float
    ) -> None:
        """
        Validate business logic constraints.
        
        Raises:
            ValidationError: If any constraint is violated
        """
        if sales_amount < 0:
            raise ValidationError(
                "sales_amount cannot be negative",
                {"sales_amount": sales_amount}
            )
        
        if target_amount <= 0:
            raise ValidationError(
                "target_amount must be greater than zero",
                {"target_amount": target_amount}
            )
    
    def _calculate_percentage(
        self,
        sales_amount: float,
        target_amount: float
    ) -> float:
        """
        Calculate what percentage of target was achieved.
        
        Uses Decimal for precision to avoid floating-point errors.
        Does NOT round here to preserve precision for threshold comparisons.
        Rounding should only happen at display time.
        """
        # Convert to Decimal for precise arithmetic
        sales_decimal = Decimal(str(sales_amount))
        target_decimal = Decimal(str(target_amount))
        
        # Calculate percentage without rounding to preserve precision
        percentage = (sales_decimal / target_decimal) * Decimal("100")
        
        return float(percentage)
    
    def _is_eligible(self, percentage_of_target: float) -> bool:
        """
        Determine if salesperson meets eligibility threshold.
        
        Args:
            percentage_of_target: Achievement percentage (e.g., 83.33 for 83.33%)
        
        Returns:
            True if eligible, False otherwise
            
        Note: Uses Decimal comparison to avoid floating-point precision issues
        with boundary conditions (e.g., 79.9999% vs 80.00%)
        """
        threshold_percentage = self.eligibility_threshold * 100
        
        # Use Decimal for precise comparison at boundary
        percentage_decimal = Decimal(str(percentage_of_target))
        threshold_decimal = Decimal(str(threshold_percentage))
        
        return percentage_decimal >= threshold_decimal
    
    def _calculate_commission_amount(
        self,
        sales_amount: float,
        eligible: bool
    ) -> float:
        """
        Calculate final commission amount.
        
        Returns 0 if not eligible, otherwise applies commission rate.
        """
        if not eligible:
            return 0.0
        
        # Use Decimal for precise monetary calculations
        sales_decimal = Decimal(str(sales_amount))
        rate_decimal = Decimal(str(self.commission_rate))
        
        commission = sales_decimal * rate_decimal
        
        # Round to 2 decimal places (currency standard)
        commission = commission.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )
        
        return float(commission)
    
    @staticmethod
    def _validate_configuration(
        commission_rate: float,
        eligibility_threshold: float
    ) -> None:
        """
        Validate service configuration at initialization.
        
        Fail-fast principle: Catch configuration errors immediately.
        """
        if not 0 <= commission_rate <= 1:
            raise BusinessRuleViolation(
                "commission_rate must be between 0 and 1",
                {"commission_rate": commission_rate}
            )
        
        if not 0 < eligibility_threshold <= 1:
            raise BusinessRuleViolation(
                "eligibility_threshold must be between 0 and 1",
                {"eligibility_threshold": eligibility_threshold}
            )


# Singleton instance with default configuration
# Can be overridden for testing or multi-tenant scenarios
commission_service = CommissionCalculatorService()
