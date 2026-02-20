"""
Test suite for FastAPI endpoints.

Testing Strategy:
- Integration tests for HTTP layer
- Input validation via Pydantic
- Error response format validation
- Status code verification
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app


class TestCommissionAPI:
    """Integration tests for commission calculation endpoint."""
    
    @pytest.fixture
    def client(self) -> TestClient:
        """Provide test client for each test."""
        return TestClient(app)
    
    # ==============================================================
    # Successful Requests
    # ==============================================================
    
    def test_valid_request_returns_200(self, client):
        """Test successful commission calculation."""
        response = client.post(
            "/api/v1/commission",
            json={
                "sales_amount": 100000.00,
                "target_amount": 120000.00
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "commission" in data
        assert "eligible" in data
        assert "percentage_of_target" in data
        
        assert data["commission"] == 5000.00
        assert data["eligible"] is True
        assert data["percentage_of_target"] == 83.33
    
    def test_ineligible_request_returns_zero_commission(self, client):
        """Test ineligible case returns commission = 0."""
        response = client.post(
            "/api/v1/commission",
            json={
                "sales_amount": 90000.00,
                "target_amount": 120000.00
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["commission"] == 0.00
        assert data["eligible"] is False
    
    # ==============================================================
    # Input Validation Testing
    # ==============================================================
    
    def test_negative_sales_returns_422(self, client):
        """Test that negative sales amount is rejected."""
        response = client.post(
            "/api/v1/commission",
            json={
                "sales_amount": -1000.00,
                "target_amount": 120000.00
            }
        )
        
        assert response.status_code == 422
        data = response.json()
        
        assert "error" in data
        assert "ValidationError" in data["error"]
    
    def test_zero_target_returns_422(self, client):
        """Test that zero target is rejected."""
        response = client.post(
            "/api/v1/commission",
            json={
                "sales_amount": 100000.00,
                "target_amount": 0.00
            }
        )
        
        assert response.status_code == 422
    
    def test_negative_target_returns_422(self, client):
        """Test that negative target is rejected."""
        response = client.post(
            "/api/v1/commission",
            json={
                "sales_amount": 100000.00,
                "target_amount": -120000.00
            }
        )
        
        assert response.status_code == 422
    
    def test_non_numeric_input_returns_422(self, client):
        """Test that non-numeric input is rejected."""
        response = client.post(
            "/api/v1/commission",
            json={
                "sales_amount": "invalid",
                "target_amount": 120000.00
            }
        )
        
        assert response.status_code == 422
    
    def test_missing_field_returns_422(self, client):
        """Test that missing required field is rejected."""
        response = client.post(
            "/api/v1/commission",
            json={
                "sales_amount": 100000.00
                # target_amount missing
            }
        )
        
        assert response.status_code == 422
    
    def test_extra_field_is_ignored(self, client):
        """Test that extra fields are ignored (not rejected)."""
        response = client.post(
            "/api/v1/commission",
            json={
                "sales_amount": 100000.00,
                "target_amount": 120000.00,
                "extra_field": "ignored"
            }
        )
        
        # Should still succeed, extra field ignored
        assert response.status_code == 200
    
    def test_extremely_large_value_returns_422(self, client):
        """Test overflow protection."""
        response = client.post(
            "/api/v1/commission",
            json={
                "sales_amount": 1e13,  # 10 trillion (exceeds MAX_AMOUNT)
                "target_amount": 120000.00
            }
        )
        
        assert response.status_code == 422
    
    # ==============================================================
    # Response Format Testing
    # ==============================================================
    
    def test_response_has_correct_structure(self, client):
        """Test response contains all required fields."""
        response = client.post(
            "/api/v1/commission",
            json={
                "sales_amount": 100000.00,
                "target_amount": 120000.00
            }
        )
        
        data = response.json()
        
        # Required fields
        assert "commission" in data
        assert "eligible" in data
        assert "percentage_of_target" in data
        
        # Type validation
        assert isinstance(data["commission"], (int, float))
        assert isinstance(data["eligible"], bool)
        assert isinstance(data["percentage_of_target"], (int, float))
    
    def test_error_response_has_correct_structure(self, client):
        """Test error responses have consistent structure."""
        response = client.post(
            "/api/v1/commission",
            json={
                "sales_amount": -1000.00,
                "target_amount": 120000.00
            }
        )
        
        data = response.json()
        
        assert "error" in data
        assert "message" in data
    
    # ==============================================================
    # Edge Cases
    # ==============================================================
    
    def test_boundary_80_percent_exactly(self, client):
        """Test critical boundary: exactly 80%."""
        response = client.post(
            "/api/v1/commission",
            json={
                "sales_amount": 96000.00,
                "target_amount": 120000.00
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["eligible"] is True
        assert data["percentage_of_target"] == 80.00
    
    # ==============================================================
    # Health Check
    # ==============================================================
    
    def test_health_check_returns_200(self, client):
        """Test health check endpoint."""
        response = client.get("/api/v1/commission/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "healthy"
    
    # ==============================================================
    # CORS Testing
    # ==============================================================
    
    def test_options_request_succeeds(self, client):
        """Test CORS preflight request."""
        response = client.options(
            "/api/v1/commission",
            headers={"Origin": "http://localhost:3000"}
        )
        
        # Should not be 405 (Method Not Allowed)
        assert response.status_code in [200, 204]
