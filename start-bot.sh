#!/bin/bash

# Production startup script for Telegram bot

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Telegram bot...${NC}"

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}Error: .env file not found!${NC}"
    echo -e "${YELLOW}Please copy .env.example to .env and fill in the required values.${NC}"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}Error: Virtual environment not found!${NC}"
    echo -e "${YELLOW}Please run start.sh first or create venv manually.${NC}"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Start the bot
echo -e "${GREEN}Starting Telegram bot...${NC}"
exec python bot.py

