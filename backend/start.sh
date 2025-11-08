#!/bin/bash
# Quick Start Script for PersonaReflect Backend

set -e

BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     PersonaReflect Backend - Quick Start Script       ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Step 1: Check if .env exists
echo -e "${BLUE}[1/5]${NC} Checking environment configuration..."
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠  .env file not found. Creating from .env.example...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created${NC}"
    echo -e "${RED}⚠  IMPORTANT: Edit backend/.env and add your GOOGLE_API_KEY!${NC}"
    echo ""
    echo "Get your API key from: https://aistudio.google.com/app/apikey"
    echo ""
    read -p "Press Enter after you've added your API key to continue..."
fi

# Check if API key is set
if grep -q "your_google_ai_api_key_here" .env; then
    echo -e "${RED}✗ GOOGLE_API_KEY not configured in .env${NC}"
    echo "Please edit backend/.env and replace 'your_google_ai_api_key_here' with your actual key"
    exit 1
fi

echo -e "${GREEN}✓ Environment configured${NC}"

# Step 2: Check Python version
echo -e "${BLUE}[2/5]${NC} Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python ${python_version}${NC}"

# Step 3: Install dependencies
echo -e "${BLUE}[3/5]${NC} Installing dependencies..."
if ! pip list | grep -q "google-adk"; then
    echo "Installing Python packages..."
    pip install -r requirements.txt
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${GREEN}✓ Dependencies already installed${NC}"
fi

# Step 4: Run tests
echo -e "${BLUE}[4/5]${NC} Running backend tests..."
echo ""
python3 test_backend.py

# Step 5: Start server
echo ""
echo -e "${BLUE}[5/5]${NC} Starting backend server..."
echo ""
echo -e "${GREEN}Backend will be available at:${NC}"
echo -e "  ${BLUE}→${NC} API: http://localhost:8000"
echo -e "  ${BLUE}→${NC} Docs: http://localhost:8000/docs"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""

uvicorn persona_reflect.main:app --reload --host 0.0.0.0 --port 8000
