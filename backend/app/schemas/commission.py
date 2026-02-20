"""
Request/Response schemas using Pydantic for automatic validation.

Design Decision: Pydantic provides:
- Automatic type validation
- JSON schema generation for OpenAPI
- Clear API contracts
- Protection against injection attacks
"""
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator
from typing_extensions import Annotated

from app.core.config import MAX_AMOUNT, MIN_AMOUNT


class CommissionRequest(BaseModel):
    """
    Request schema for commission calculation.
    
    Constraints:
    - sales_amount: Must be non-negative, < MAX_AMOUNT
    - target_amount: Must be positive (> 0), < MAX_AMOUNT
    """
    
    sales_amount: Annotated[
        float,
        Field(
            ge=MIN_AMOUNT,
            le=MAX_AMOUNT,
            description="Actual sales amount achieved",
            examples=[100000.00]
        )
    ]
    
    target_amount: Annotated[
        float,
        Field(
            gt=MIN_AMOUNT,  # Must be > 0, not >= 0
            le=MAX_AMOUNT,
            description="Sales target amount",
            examples=[120000.00]
        )
    ]
    
    @field_validator("sales_amount", "target_amount")
    @classmethod
    def validate_numeric_precision(cls, value: float) -> float:
        """
        Ensure values don't have excessive decimal precision.
        Prevents floating-point arithmetic issues.
        """
        # Round to 2 decimal places (currency standard)
        rounded = round(value, 2)
        return rounded
    
    @field_validator("target_amount")
    @classmethod
    def validate_target_not_zero(cls, value: float) -> float:
        """Ensure target is never zero (prevents division by zero)."""
        if value <= 0:
            raise ValueError("target_amount must be greater than zero")
        return value
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sales_amount": 100000.00,
                    "target_amount": 120000.00
                },
                {
                    "sales_amount": 95000.50,
                    "target_amount": 120000.00
                }
            ]
        }
    }


class CommissionResponse(BaseModel):
    """
    Response schema for commission calculation.
    
    Returns:
    - commission: Calculated commission amount
    - eligible: Whether the salesperson is eligible for commission
    - percentage_of_target: What % of target was achieved
    """
    
    commission: Annotated[
        float,
        Field(
            ge=0.0,
            description="Calculated commission amount",
            examples=[5000.00]
        )
    ]
    
    eligible: Annotated[
        bool,
        Field(
            description="Whether commission eligibility threshold was met",
            examples=[True]
        )
    ]
    
    percentage_of_target: Annotated[
        float,
        Field(
            ge=0.0,
            le=1000.0,  # Allow > 100% (over-achievement)
            description="Percentage of target achieved",
            examples=[83.33]
        )
    ]
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "commission": 5000.00,
                    "eligible": True,
                    "percentage_of_target": 83.33
                },
                {
                    "commission": 0.00,
                    "eligible": False,
                    "percentage_of_target": 75.00
                }
            ]
        }
    }


class ErrorResponse(BaseModel):
    """Standard error response structure."""
    
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Human-readable error message")
    details: dict | None = Field(None, description="Additional error context")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": "ValidationError",
                    "message": "Invalid input data",
                    "details": {"field": "target_amount", "issue": "must be greater than zero"}
                }
            ]
        }
    }
