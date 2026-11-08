#!/usr/bin/env bash
# ─────────────────────────────────────────────
#  OrinCron — Startup Script
# ─────────────────────────────────────────────

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Load .env if it exists
if [ -f ".env" ]; then
  echo "[OrinCron] Loading .env file..."
  export $(grep -v '^#' .env | grep -v '^$' | xargs)
else
  echo "[OrinCron] WARNING: No .env file found. Copy .env.example to .env and fill in your values."
fi

# Check Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
  echo "[OrinCron] ERROR: Python is not installed."
  exit 1
fi

PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
  PYTHON_CMD="python"
fi

# Create data directory if needed
mkdir -p data

# Install dependencies if needed
if [ ! -d "venv" ]; then
  echo "[OrinCron] Creating virtual environment..."
  $PYTHON_CMD -m venv venv
fi

echo "[OrinCron] Activating virtual environment..."
source venv/bin/activate || source venv/Scripts/activate 2>/dev/null || true

echo "[OrinCron] Installing dependencies..."
pip install -q -r requirements.txt

echo "[OrinCron] Starting OrinCron bot..."
python orin.py
