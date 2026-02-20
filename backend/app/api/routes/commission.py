"""
Commission calculation API endpoints.

Design Pattern: Thin controller - delegates to service layer.
Responsibilities:
- HTTP request/response handling
- Input validation (via Pydantic)
- Error transformation
- OpenAPI documentation
"""
from fastapi import APIRouter, status, HTTPException, Response
from fastapi.responses import JSONResponse

from app.schemas import CommissionRequest, CommissionResponse, ErrorResponse
from app.services import commission_service
from app.core.exceptions import ValidationError, BusinessRuleViolation

router = APIRouter(prefix="/commission", tags=["Commission"])


@router.post(
    "",
    response_model=CommissionResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Commission calculated successfully",
            "model": CommissionResponse,
        },
        400: {
            "description": "Invalid input data",
            "model": ErrorResponse,
        },
        422: {
            "description": "Validation error",
            "model": ErrorResponse,
        },
        500: {
            "description": "Internal server error",
            "model": ErrorResponse,
        },
    },
    summary="Calculate sales commission",
    description="""
    Calculate commission based on sales performance.
    
    **Business Rules:**
    - If sales < 80% of target → commission = 0
    - If sales ≥ 80% of target → commission = 5% of sales
    
    **Input Constraints:**
    - sales_amount: Must be non-negative
    - target_amount: Must be positive (> 0)
    - Both values must be < 1 trillion (overflow protection)
    
    **Example:**
    ```
    Request: {"sales_amount": 100000, "target_amount": 120000}
    Response: {"commission": 5000.0, "eligible": true, "percentage_of_target": 83.33}
    ```
    """,
)
async def calculate_commission(
    request: CommissionRequest,
) -> CommissionResponse:
    """
    Calculate commission for sales performance.
    
    This endpoint is the primary interface for commission calculation.
    It delegates business logic to the service layer and handles HTTP concerns.
    
    Args:
        request: Commission calculation request with sales and target amounts
    
    Returns:
        CommissionResponse with calculated commission and eligibility status
    
    Raises:
        HTTPException: For validation errors or business rule violations
    """
    try:
        # Delegate to service layer (pure business logic)
        result = commission_service.calculate_commission(
            sales_amount=request.sales_amount,
            target_amount=request.target_amount,
        )
        
        # Transform service result to API response
        return CommissionResponse(
            commission=result.commission,
            eligible=result.eligible,
            percentage_of_target=result.percentage_of_target,
        )
    
    except (ValidationError, BusinessRuleViolation) as e:
        # Transform domain exceptions to HTTP 400
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": e.__class__.__name__,
                "message": e.message,
                "details": e.details,
            },
        )
    
    except Exception as e:
        # Catch-all for unexpected errors (log in production)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "InternalServerError",
                "message": "An unexpected error occurred",
                "details": {"error_type": str(type(e).__name__)},
            },
        )


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Check if the commission service is operational",
    tags=["Health"],
)
async def health_check() -> dict[str, str]:
    """
    Health check endpoint for monitoring and load balancers.
    
    Returns:
        Status indicating service health
    """
    return {"status": "healthy", "service": "commission-calculator"}


@router.options(
    "",
    status_code=status.HTTP_200_OK,
    summary="CORS preflight",
    description="Handle CORS preflight requests",
    include_in_schema=False,
)
async def commission_options() -> Response:
    """
    Handle CORS preflight OPTIONS request.
    
    This endpoint is required for browsers to perform CORS preflight checks
    before making POST requests from different origins.
    
    Returns:
        Empty response with appropriate CORS headers (set by middleware)
    """
    return Response(status_code=status.HTTP_200_OK)
