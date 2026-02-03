#!/bin/bash
# Start script for SEO-SWARM Frontend

set -e

echo "🚀 Starting SEO-SWARM Frontend..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if in frontend directory
if [ ! -f "package.json" ]; then
    echo "${YELLOW}Not in frontend directory. Navigating...${NC}"
    cd "$(dirname "$0")"
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "${BLUE}Checking prerequisites...${NC}"

if ! command_exists python3; then
    echo "${YELLOW}Python 3 is required but not installed.${NC}"
    exit 1
fi

if ! command_exists node; then
    echo "${YELLOW}Node.js is required but not installed.${NC}"
    exit 1
fi

echo "${GREEN}✓ Prerequisites OK${NC}"

# Backend setup
echo "${BLUE}Setting up backend...${NC}"
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null

echo "Installing backend dependencies..."
pip install -q -r requirements.txt

echo "${GREEN}✓ Backend ready${NC}"

# Start backend in background
echo "${BLUE}Starting backend server...${NC}"
python main.py &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

cd ..

# Frontend setup
echo "${BLUE}Setting up frontend...${NC}"

if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

echo "${GREEN}✓ Frontend ready${NC}"

# Start frontend
echo "${BLUE}Starting frontend dev server...${NC}"
echo ""
echo "${GREEN}Dashboard will be available at:${NC}"
echo "${BLUE}  Frontend: http://localhost:5173${NC}"
echo "${BLUE}  Backend:  http://localhost:8000${NC}"
echo "${BLUE}  API Docs: http://localhost:8000/docs${NC}"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Trap to cleanup on exit
cleanup() {
    echo ""
    echo "${YELLOW}Shutting down...${NC}"
    kill $BACKEND_PID 2>/dev/null || true
    exit 0
}

trap cleanup INT TERM

# Start frontend (foreground)
npm run dev

# Cleanup if we exit normally
cleanup
