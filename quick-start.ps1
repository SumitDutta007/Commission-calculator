# Quick Start Script for Dynamic Incentive Calculator (Windows)
# Run with: .\quick-start.ps1

Write-Host "🚀 Dynamic Incentive Calculator - Quick Start" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host ""

# Check prerequisites
Write-Host "📋 Checking prerequisites..." -ForegroundColor Yellow

try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python 3.11+ required but not installed. Aborting." -ForegroundColor Red
    exit 1
}

try {
    $nodeVersion = node --version 2>&1
    Write-Host "✅ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js 20+ required but not installed. Aborting." -ForegroundColor Red
    exit 1
}

try {
    $dockerVersion = docker --version 2>&1
    Write-Host "✅ Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Docker not found. Docker deployment will not be available." -ForegroundColor Yellow
}

Write-Host ""

# Backend setup
Write-Host "🐍 Setting up Backend..." -ForegroundColor Cyan
Set-Location backend

if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

Write-Host "Installing dependencies..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

Write-Host "Running backend tests..." -ForegroundColor Yellow
pytest --cov=app --cov-fail-under=90 -v

Write-Host "✅ Backend setup complete" -ForegroundColor Green
Write-Host ""

# Deactivate venv
deactivate

# Return to root
Set-Location ..

# Frontend setup
Write-Host "⚛️  Setting up Frontend..." -ForegroundColor Cyan
Set-Location frontend

if (-not (Test-Path "node_modules")) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    npm install
}

if (-not (Test-Path ".env.local")) {
    Write-Host "Creating .env.local..." -ForegroundColor Yellow
    Copy-Item .env.local.example .env.local
}

Write-Host "Running frontend tests..." -ForegroundColor Yellow
npm test -- --passWithNoTests

Write-Host "✅ Frontend setup complete" -ForegroundColor Green
Write-Host ""

# Return to root
Set-Location ..

Write-Host "🎉 Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Quick Commands:" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend:" -ForegroundColor Yellow
Write-Host "  cd backend"
Write-Host "  .\venv\Scripts\Activate.ps1"
Write-Host "  uvicorn app.main:app --reload"
Write-Host "  → http://localhost:8000"
Write-Host "  → http://localhost:8000/docs (API Documentation)"
Write-Host ""
Write-Host "Frontend:" -ForegroundColor Yellow
Write-Host "  cd frontend"
Write-Host "  npm run dev"
Write-Host "  → http://localhost:3000"
Write-Host ""
Write-Host "Docker (All-in-One):" -ForegroundColor Yellow
Write-Host "  docker-compose up --build"
Write-Host "  → Frontend: http://localhost:3000"
Write-Host "  → Backend: http://localhost:8000"
Write-Host ""
Write-Host "Run Tests:" -ForegroundColor Yellow
Write-Host "  Backend: cd backend; pytest"
Write-Host "  Frontend: cd frontend; npm test"
Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Cyan
Write-Host "  README.md - Comprehensive project documentation"
Write-Host "  ARCHITECTURE.md - Architecture decision records"
Write-Host "  CONTRIBUTING.md - Contribution guidelines"
Write-Host ""
Write-Host "Happy coding! 🎯" -ForegroundColor Green
