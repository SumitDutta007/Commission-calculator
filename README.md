# Dynamic Incentive Calculator

A production-grade, full-stack commission calculation system built with clean architecture, comprehensive testing, and DevOps best practices. Calculates sales commissions based on target achievement with an 80% eligibility threshold and 5% commission rate.

## 🚀 Live Demo

- **Frontend**: [https://commission-calculator-git-main-sumitdutta007s-projects.vercel.app/](https://commission-calculator-git-main-sumitdutta007s-projects.vercel.app/)
- **Backend API**: [https://incentive-calculator-api.onrender.com](https://incentive-calculator-api.onrender.com)
- **API Documentation**: [https://incentive-calculator-api.onrender.com/docs](https://incentive-calculator-api.onrender.com/docs) (Interactive Swagger UI)
- **Health Check**: [https://incentive-calculator-api.onrender.com/api/v1/commission/health](https://incentive-calculator-api.onrender.com/api/v1/commission/health)

## ✅ Assignment Requirements Met

**Task**: Create a single API-endpoint solution that accepts Sales_Amount and Target_Amount as inputs and returns the resulting Commission.


## 🏗️ Architecture Overview

### High-Level Design

```
┌─────────────┐      HTTP/REST      ┌─────────────┐
│   Next.js   │ ◄──────────────────► │   FastAPI   │
│  Frontend   │   JSON Requests      │   Backend   │
└─────────────┘                      └─────────────┘
      │                                     │
      │                                     │
      ▼                                     ▼
 React Client                         Clean Architecture
 - UI Components                      - Service Layer
 - Custom Hooks                       - API Routes
 - Type Safety                        - Core Domain
 - Client Validation                  - Schema Validation
```

### Backend Architecture

```
app/
├── core/              # Domain Layer
│   ├── config.py      # Business rules & configuration
│   └── exceptions.py  # Domain exceptions
│
├── schemas/           # Interface Adapters
│   └── commission.py  # Pydantic models (API contract)
│
├── services/          # Application Layer (Pure Business Logic)
│   └── commission_service.py  # Commission calculation
│
└── api/               # Infrastructure Layer
    └── routes/        # HTTP controllers
        └── commission.py
```


### Frontend Architecture

```
frontend/
├── app/               # Next.js App Router
│   ├── page.tsx       # Home page
│   └── layout.tsx     # Root layout
│
├── components/        # Presentation Layer
│   └── CommissionCalculator.tsx
│
├── hooks/             # Business Logic Hooks
│   └── useCommissionCalculator.ts
│
└── services/          # API Integration
    └── api.ts         # HTTP client
```

## 🎯 Business Rules

### Commission Calculation Logic

**Rule**: Sales representatives earn commission based on target achievement.

- **Eligibility Threshold**: ≥80% of target
- **Commission Rate**: 5% of sales amount
- **Below Threshold**: No commission

**Examples**:
```
Sales: $100,000 | Target: $120,000 | Achievement: 83.33% | Commission: $5,000 ✓
Sales: $60,000  | Target: $100,000 | Achievement: 60.00% | Commission: $0 ✗
Sales: $96,000  | Target: $120,000 | Achievement: 80.00% | Commission: $4,800 ✓
```

## 🛠️ Technology Stack

### Backend: FastAPI
**Why FastAPI over Django?**
- **Performance**: 3x faster than Django (ASGI vs WSGI)
- **Modern Python**: Native async/await, type hints
- **Auto Documentation**: OpenAPI/Swagger out-of-the-box
- **Validation**: Pydantic integration (faster than Django serializers)
- **Microservices Ready**: Lightweight, no batteries-included overhead
- **Developer Experience**: Hot reload, auto-completion

**Trade-offs**:
- Django better for: Admin panel, ORM, monolithic apps
- FastAPI better for: APIs, microservices, performance-critical apps

### Frontend: Next.js 14
**Why Next.js over Create React App?**
- **Production Ready**: Built-in optimization, image optimization
- **Server Components**: Better performance, reduced JS bundle
- **App Router**: Modern routing with layouts
- **TypeScript**: First-class support
- **Developer Experience**: Fast refresh, built-in CSS support

### Testing Frameworks
- **Backend**: pytest (Python standard, powerful fixtures)
- **Frontend**: Jest + React Testing Library (industry standard)

### DevOps
- **Containerization**: Docker (multi-stage builds)
- **Orchestration**: Docker Compose (local development)
- **CI/CD**: GitHub Actions (free, integrated)

## 📊 Code Quality & Testing


**Test Categories**:
1. **Edge Cases**
   - Zero sales
   - Sales exceeding target
   - Large numbers (near MAX_AMOUNT)
   - Decimal precision

2. **Error Path Testing**
   - Negative values
   - Zero target
   - Invalid configurations

**Running Tests**:
```bash
cd backend
pytest                    # Run all tests
pytest --cov=app         # With coverage
pytest -v                # Verbose output
pytest -k "boundary"     # Run specific tests
```

### Frontend Testing Strategy

**Coverage**: 80%+ required

**Test Categories**:
1. **Component Tests**: Rendering, user interactions
2. **Hook Tests**: State management, API integration
3. **API Tests**: Mocking, error handling
4. **Accessibility Tests**: ARIA labels, keyboard navigation

**Running Tests**:
```bash
cd frontend
npm test                 # Run all tests
npm run test:watch      # Watch mode
npm run test:coverage   # With coverage
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js 20+
- Docker & Docker Compose (optional)

### Local Development (Without Docker)

**Backend**:
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend**:
```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.local.example .env.local

# Run tests
npm test

# Start development server
npm run dev
```

**Access**:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Docker Development

**Start all services**:
```bash
docker-compose up --build
```

**Access**:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

**Stop services**:
```bash
docker-compose down
```

### Production Deployment

**Build production images**:
```bash
# Backend
docker build -t incentive-calculator-backend:latest ./backend

# Frontend
docker build -t incentive-calculator-frontend:latest ./frontend
```

**Deploy with Docker Compose**:
```bash
docker-compose up -d
```

## 📡 API Contract

### Calculate Commission

**Endpoint**: `POST /api/v1/commission`

**Request**:
```json
{
  "sales_amount": 100000.00,
  "target_amount": 120000.00
}
```

**Response (Success - 200)**:
```json
{
  "commission": 5000.00,
  "eligible": true,
  "percentage_of_target": 83.33
}
```

**Response (Validation Error - 422)**:
```json
{
  "error": "ValidationError",
  "message": "Target amount must be greater than zero",
  "details": {
    "field": "target_amount",
    "constraint": "greater_than_zero"
  }
}
```

**Validation Rules**:
- `sales_amount`: ≥ 0, ≤ 1e12 (1 trillion)
- `target_amount`: > 0, ≤ 1e12
- Both: 2 decimal places maximum

### Health Check

**Endpoint**: `GET /api/v1/commission/health`

**Response**:
```json
{
  "status": "healthy"
}
```

## 🔒 Security Considerations

### Backend
- **Input Validation**: Pydantic schemas with custom validators
- **Decimal Arithmetic**: Avoid floating-point errors
- **Overflow Protection**: MAX_AMOUNT constraint (1e12)
- **Exception Handling**: Custom exceptions, no sensitive info leak
- **Non-Root User**: Docker runs as `appuser:appuser`

### Frontend
- **Client-Side Validation**: Prevent invalid API calls
- **Type Safety**: TypeScript throughout
- **XSS Protection**: React's built-in escaping
- **CORS**: Configured in backend

## 📈 Scalability Considerations

### Current Implementation
- **Backend**: 4 uvicorn workers (CPU-bound)
- **Stateless**: No session storage, horizontally scalable
- **Container-Ready**: Docker images for orchestration

### Scaling Strategies (For future)

**Vertical Scaling**:
```python
# Increase workers based on CPU cores
workers = (2 * cpu_count) + 1
uvicorn app.main:app --workers 8
```

**Horizontal Scaling**:
```yaml
# Kubernetes example
apiVersion: apps/v1
kind: Deployment
spec:
  replicas: 5
  template:
    spec:
      containers:
      - name: backend
        image: incentive-calculator-backend:latest
        resources:
          requests:
            cpu: "500m"
            memory: "512Mi"
          limits:
            cpu: "1000m"
            memory: "1Gi"
```

**Load Balancing**:
- **Nginx**: Reverse proxy with health checks
- **AWS ALB**: Managed load balancer
- **Kubernetes Ingress**: Native load balancing

**Caching Strategy** (if needed):
```python
# Redis cache for complex calculations
@cache(ttl=300)
def calculate_commission_cached(sales, target):
    return calculate_commission(sales, target)
```

**Database Integration** (future enhancement):
```
┌──────────┐
│ Frontend │
└────┬─────┘
     │
     ▼
┌──────────┐      ┌──────────┐
│  FastAPI │ ───► │ MongoDB  │
└──────────┘      │ /Postgres│
                  └──────────┘
```

**Monitoring & Observability**:
- **Metrics**: Prometheus + Grafana
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)
- **Tracing**: OpenTelemetry
- **Alerting**: PagerDuty, Slack integration

## 🧪 CI/CD Pipeline

### GitHub Actions Workflow

**Triggers**:
- Push to `main` or `develop`
- Pull requests to `main` or `develop`

**Jobs**:
1. **Backend Tests & Linting**
   - Ruff linting (format + check)
   - pytest with 90% coverage requirement
   - Upload coverage to Codecov

2. **Frontend Tests & Linting**
   - ESLint
   - Jest tests with 80% coverage
   - Upload coverage to Codecov

3. **Docker Build Verification**
   - Build backend image
   - Build frontend image
   - Cache layers for speed

4. **Integration Tests**
   - Start services with Docker Compose
   - Health checks
   - End-to-end API testing

**Failure Handling**:
- Any job failure stops deployment
- Coverage below threshold = build fails
- Lint errors = build fails

## 🤝 Design Decisions

### 1. Why Decimal for Money?
```python
# BAD: Floating point errors
0.1 + 0.2 = 0.30000000000000004

# GOOD: Exact decimal arithmetic
Decimal('0.1') + Decimal('0.2') = Decimal('0.3')
```

### 2. Why Service Layer?
**Without Service Layer**:
```python
# Tightly coupled to FastAPI
@app.post("/commission")
def calculate(request: CommissionRequest):
    if request.sales_amount >= request.target_amount * 0.8:
        return request.sales_amount * 0.05
    return 0
```

**With Service Layer**:
```python
# Framework-agnostic, testable
class CommissionCalculatorService:
    def calculate_commission(self, sales, target):
        # Pure business logic
        pass

# Easy to test
def test_service():
    service = CommissionCalculatorService()
    result = service.calculate_commission(100, 120)
```

### 3. Why Custom Exceptions?
```python
# Generic exceptions lose context
raise ValueError("Invalid amount")

# Custom exceptions are semantic
raise ValidationError(
    message="Target amount must be positive",
    details={"field": "target_amount", "value": -100}
)
```

### 4. Why React Hooks?
```python
# Reusable logic across components
const { result, loading, error, calculate } = useCommissionCalculator();

# Instead of duplicating:
const [result, setResult] = useState(null);
const [loading, setLoading] = useState(false);
// ... repeated in every component
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Clean Architecture by Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [12-Factor App Methodology](https://12factor.net/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## 📄 License

MIT License - This is a demonstration project for technical evaluation.

---

**Built with** ❤️ **for principal-level engineering evaluation**
