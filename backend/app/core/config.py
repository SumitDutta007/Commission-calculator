"""
Core application configuration.

This module centralizes all business rules and system configuration,
making them easily modifiable without touching business logic.
Following the Open-Closed Principle (SOLID).
"""
from typing import Final
from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings with environment variable support.
    
    Design Decision: Using pydantic-settings for type-safe configuration
    that can be overridden via environment variables in different environments.
    """
    
    # Application Metadata
    APP_NAME: str = "Dynamic Incentive Calculator"
    APP_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # Business Rules (Configurable for different markets/products)
    COMMISSION_RATE: float = 0.05  # 5%
    ELIGIBILITY_THRESHOLD: float = 0.80  # 80% of target
    
    # Validation Constraints
    MAX_AMOUNT: float = 1e12  # 1 trillion - prevents overflow attacks
    MIN_AMOUNT: float = 0.0
    DECIMAL_PRECISION: int = 2
    
    # CORS Settings - Can be set as string "*" or JSON array or comma-separated
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
    ]
    
    @field_validator('ALLOWED_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse ALLOWED_ORIGINS from string or list"""
        if isinstance(v, str):
            # If it's "*", return as single-item list
            if v == "*":
                return ["*"]
            # If it's comma-separated, split it
            if "," in v:
                return [origin.strip() for origin in v.split(",")]
            # Otherwise, single origin
            return [v]
        return v
    
    # API Rate Limiting (for future implementation)
    RATE_LIMIT_PER_MINUTE: int = 100
    
    # Observability
    LOG_LEVEL: str = "INFO"
    ENABLE_METRICS: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Singleton instance
settings = Settings()


# Business Rule Constants (Type-safe)
COMMISSION_RATE: Final[float] = settings.COMMISSION_RATE
ELIGIBILITY_THRESHOLD: Final[float] = settings.ELIGIBILITY_THRESHOLD
MAX_AMOUNT: Final[float] = settings.MAX_AMOUNT
MIN_AMOUNT: Final[float] = settings.MIN_AMOUNT
