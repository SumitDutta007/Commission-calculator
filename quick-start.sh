#!/bin/bash

# Quick Start Script for Dynamic Incentive Calculator
# This script sets up the entire development environment

set -e  # Exit on error

echo "🚀 Dynamic Incentive Calculator - Quick Start"
echo "=============================================="
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."

command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3.11+ required but not installed. Aborting."; exit 1; }
command -v node >/dev/null 2>&1 || { echo "❌ Node.js 20+ required but not installed. Aborting."; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "⚠️  Docker not found. Docker deployment will not be available."; }

echo "✅ Prerequisites check complete"
echo ""

# Backend setup
echo "🐍 Setting up Backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo "Running backend tests..."
pytest --cov=app --cov-fail-under=90 -v

echo "✅ Backend setup complete"
echo ""

# Return to root
cd ..

# Frontend setup
echo "⚛️  Setting up Frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

if [ ! -f ".env.local" ]; then
    echo "Creating .env.local..."
    cp .env.local.example .env.local
fi

echo "Running frontend tests..."
npm test -- --passWithNoTests

echo "✅ Frontend setup complete"
echo ""

# Return to root
cd ..

echo "🎉 Setup Complete!"
echo ""
echo "📝 Quick Commands:"
echo ""
echo "Backend:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload"
echo "  → http://localhost:8000"
echo "  → http://localhost:8000/docs (API Documentation)"
echo ""
echo "Frontend:"
echo "  cd frontend"
echo "  npm run dev"
echo "  → http://localhost:3000"
echo ""
echo "Docker (All-in-One):"
echo "  docker-compose up --build"
echo "  → Frontend: http://localhost:3000"
echo "  → Backend: http://localhost:8000"
echo ""
echo "Run Tests:"
echo "  Backend: cd backend && pytest"
echo "  Frontend: cd frontend && npm test"
echo ""
echo "📚 Documentation:"
echo "  README.md - Comprehensive project documentation"
echo "  ARCHITECTURE.md - Architecture decision records"
echo "  CONTRIBUTING.md - Contribution guidelines"
echo ""
echo "Happy coding! 🎯"
