#!/bin/bash

# Performance Review Tracker - Web UI Startup Script
# This script starts the Flask web interface for the performance review tracker

set -e  # Exit on any error

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🚀 Starting Performance Review Tracker Web UI"
echo "Project root: $PROJECT_ROOT"

# Change to project root directory
cd "$PROJECT_ROOT"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first:"
    echo "   python -m venv venv"
    echo "   source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
else
    echo "❌ Cannot find virtual environment activation script"
    exit 1
fi

# Check if Flask is installed
if ! python -c "import flask" 2>/dev/null; then
    echo "❌ Flask not found. Installing dependencies..."
    pip install -r requirements.txt
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p ui/uploads
mkdir -p ui/results

# Set environment variables
export FLASK_APP=ui/app.py
export FLASK_ENV=development
export FLASK_DEBUG=1

# Check if port is specified
PORT=${1:-8888}

echo "🌐 Starting Flask development server on port $PORT..."
echo "📱 Open your browser to: http://localhost:$PORT"
echo "⏹️  Press Ctrl+C to stop the server"
echo ""

# Start Flask development server with specified port
python ui/app.py $PORT