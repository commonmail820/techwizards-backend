#!/bin/bash

# Start script for Mexican Restaurant Backend API
echo "🚀 Starting Mexican Restaurant Backend API..."
echo "📍 Server will be available at: http://localhost:8001"
echo "📖 API Documentation: http://localhost:8001/docs"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python -m venv venv
    echo "✅ Virtual environment created."
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Please copy env.example to .env and configure it."
    echo "   cp env.example .env"
    echo "   Then edit .env with your Supabase credentials."
    exit 1
fi

# Start the server
echo "🎯 Starting FastAPI server..."
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} 