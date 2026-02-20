"""
Custom exception hierarchy for domain-specific errors.

Design Pattern: Custom exceptions for better error handling and debugging.
Each exception carries semantic meaning about what went wrong.
"""
from typing import Any


class IncentiveCalculatorException(Exception):
    """Base exception for all domain-specific errors."""
    
    def __init__(self, message: str, details: dict[str, Any] | None = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(IncentiveCalculatorException):
    """Raised when input validation fails."""
    pass


class BusinessRuleViolation(IncentiveCalculatorException):
    """Raised when business logic constraints are violated."""
    pass


class ConfigurationError(IncentiveCalculatorException):
    """Raised when system configuration is invalid."""
    pass
