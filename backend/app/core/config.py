"""
Core application configuration.

This module centralizes all business rules and system configuration,
making them easily modifiable without touching business logic.
Following the Open-Closed Principle (SOLID).
"""
from typing import Final, Union
from pydantic import field_validator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings with environment variable support.
    
    Design Decision: Using pydantic-settings for type-safe configuration
    that can be overridden via environment variables in different environments.
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra='ignore'
    )
    
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
    
    # CORS Settings - Accept string or list, will be normalized to list
    ALLOWED_ORIGINS: Union[str, list[str]] = Field(
        default=[
            "http://localhost:3000",
            "http://localhost:3001",
            "http://127.0.0.1:3000",
        ]
    )
    
    @field_validator('ALLOWED_ORIGINS')
    @classmethod
    def parse_origins(cls, v: Union[str, list[str]]) -> list[str]:
        """Parse ALLOWED_ORIGINS from string to list"""
        if isinstance(v, str):
            # Handle wildcard
            if v == "*":
                return ["*"]
            # Handle comma-separated
            elif "," in v:
                return [o.strip() for o in v.split(",") if o.strip()]
            # Handle single origin
            else:
                return [v]
        return v
    
    # API Rate Limiting (for future implementation)
    RATE_LIMIT_PER_MINUTE: int = 100
    
    # Observability
    LOG_LEVEL: str = "INFO"
    ENABLE_METRICS: bool = True


# Singleton instance
settings = Settings()


# Business Rule Constants (Type-safe)
COMMISSION_RATE: Final[float] = settings.COMMISSION_RATE
ELIGIBILITY_THRESHOLD: Final[float] = settings.ELIGIBILITY_THRESHOLD
MAX_AMOUNT: Final[float] = settings.MAX_AMOUNT
MIN_AMOUNT: Final[float] = settings.MIN_AMOUNT
