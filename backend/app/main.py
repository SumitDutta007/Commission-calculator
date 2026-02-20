"""
FastAPI application factory.

Design Decisions:
- Application factory pattern for testability
- Centralized exception handling
- CORS middleware for frontend integration
- Automatic OpenAPI documentation
- Health check endpoint for orchestration
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from app.core.config import settings
from app.core.exceptions import IncentiveCalculatorException
from app.api import commission_router


def create_application() -> FastAPI:
    """
    Application factory pattern.
    
    Benefits:
    - Easier testing (can create multiple app instances)
    - Configuration flexibility
    - Cleaner separation of concerns
    """
    
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="""
        Production-grade microservice for dynamic commission calculation.
        
        ## Business Rules
        - Eligibility threshold: 80% of target
        - Commission rate: 5% of sales
        - Configurable via environment variables
        
        ## Features
        - Input validation with Pydantic
        - Precise decimal arithmetic
        - Comprehensive error handling
        - OpenAPI documentation
        - CORS support for SPA frontend
        
        ## Architecture
        - Clean Architecture pattern
        - Service layer separation
        - Domain-driven design
        - Dependency injection ready
        """,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    )
    
    # Configure CORS for frontend access
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
    
    # Register exception handlers
    register_exception_handlers(app)
    
    # Register routers
    app.include_router(
        commission_router,
        prefix=settings.API_V1_PREFIX,
    )
    
    # Root endpoint
    @app.get("/", tags=["Root"])
    async def root():
        """Root endpoint with API information."""
        return {
            "service": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "docs": "/docs",
            "health": f"{settings.API_V1_PREFIX}/commission/health",
        }
    
    return app


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register custom exception handlers.
    
    Provides consistent error responses across the application.
    """
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
    ) -> JSONResponse:
        """
        Handle Pydantic validation errors.
        
        Transforms validation errors into user-friendly messages.
        """
        errors = exc.errors()
        
        # Extract first error for simplicity
        first_error = errors[0] if errors else {}
        field = " -> ".join(str(x) for x in first_error.get("loc", []))
        message = first_error.get("msg", "Validation error")
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "ValidationError",
                "message": f"Invalid input for field '{field}': {message}",
                "details": {
                    "field": field,
                    "errors": errors,
                },
            },
        )
    
    @app.exception_handler(IncentiveCalculatorException)
    async def domain_exception_handler(
        request: Request,
        exc: IncentiveCalculatorException
    ) -> JSONResponse:
        """
        Handle domain-specific exceptions.
        
        Maps domain errors to appropriate HTTP status codes.
        """
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": exc.__class__.__name__,
                "message": exc.message,
                "details": exc.details,
            },
        )
    
    @app.exception_handler(Exception)
    async def generic_exception_handler(
        request: Request,
        exc: Exception
    ) -> JSONResponse:
        """
        Catch-all exception handler.
        
        In production, this should log to monitoring system (Sentry, CloudWatch, etc.)
        """
        # TODO: Log to monitoring system
        # logger.exception("Unhandled exception", exc_info=exc)
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "InternalServerError",
                "message": "An unexpected error occurred. Please contact support.",
                "details": {
                    "error_type": exc.__class__.__name__,
                    # Don't expose internal details in production
                    # "error_message": str(exc),
                },
            },
        )


# Application instance
app = create_application()


# For local development and testing
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
