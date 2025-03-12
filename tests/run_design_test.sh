#!/bin/bash

echo "Cleaning up Python processes..."
# Kill any existing Python processes
pkill -9 -f python 2>/dev/null || true
ps aux | grep python | grep -v grep | awk '{print $2}' | xargs kill -9 2>/dev/null || true

echo "Waiting for processes to clean up..."
sleep 2

echo "Activating virtual environment..."
# Activate virtual environment
source venv/bin/activate

echo "Running test with unbuffered output..."
# Run the test with unbuffered output and debug logging
PYTHONUNBUFFERED=1 PYTHONPATH=. python -u tests/test_design_entry.py 2>&1
