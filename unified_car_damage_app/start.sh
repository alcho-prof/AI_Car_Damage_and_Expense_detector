#!/usr/bin/env bash
# Quick launcher for AutoDamage AI Unified Application

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=================================================="
echo " Starting AutoDamage AI Unified Platform"
echo "=================================================="
echo "Directory: $SCRIPT_DIR"
echo "Server URL: http://localhost:5001"
echo "=================================================="

# Check if virtual environment exists
if [ -f "$SCRIPT_DIR/venv/bin/python" ]; then
    "$SCRIPT_DIR/venv/bin/python" "$SCRIPT_DIR/app.py"
else
    echo "Error: Virtual environment not found in $SCRIPT_DIR/venv"
    echo "Running system python..."
    python3 "$SCRIPT_DIR/app.py"
fi
