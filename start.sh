#!/bin/bash

# Production startup script for Remont application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Remont application...${NC}"

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}Error: .env file not found!${NC}"
    echo -e "${YELLOW}Please copy .env.example to .env and fill in the required values.${NC}"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${GREEN}Activating virtual environment...${NC}"
source venv/bin/activate

# Install/update Python dependencies
echo -e "${GREEN}Installing Python dependencies...${NC}"
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Install/update Node dependencies
echo -e "${GREEN}Installing Node dependencies...${NC}"
npm install --silent

# Build Tailwind CSS
echo -e "${GREEN}Building Tailwind CSS...${NC}"
npm run build

# Check if database exists, if not it will be created on first run
echo -e "${GREEN}Database will be initialized on first run...${NC}"

# Start the application
echo -e "${GREEN}Starting FastAPI application...${NC}"
echo -e "${YELLOW}Application will be available at http://0.0.0.0:8000${NC}"

# Use uvicorn with production settings
exec uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

