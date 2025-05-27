#!/bin/bash

# Amazon Product Scraper API - Quick Start Script
# This script will set up and run the API automatically

set -e  # Exit on any error

echo "🚀 Amazon Product Scraper API - Quick Start"
echo "==========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Please run this script from the amazon-product-scraper-by-asin directory"
    exit 1
fi

# Install uv if not present
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
    
    # Check if uv is now available
    if ! command -v uv &> /dev/null; then
        echo "⚠️  uv installation may need a shell restart. Trying pip install..."
        python3 -m pip install uv
    fi
fi

echo "✅ uv package manager ready"

# Create virtual environment
echo "🔧 Setting up virtual environment..."
uv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
uv pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating environment configuration..."
    cat > .env << EOF
# Server Configuration
PORT=8080
FLASK_DEBUG=True

# Rate Limiting (use memory for development)
REDIS_URL=memory://

# Scraping Configuration
REQUEST_DELAY=2
MAX_RETRIES=3
TIMEOUT=10
EOF
    echo "✅ Environment file created"
else
    echo "✅ Environment file already exists"
fi

# Run tests to verify everything works
echo "🧪 Running tests to verify setup..."
python -m pytest tests/ -v --tb=short

if [ $? -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "⚠️  Some tests failed, but the API should still work"
fi

echo ""
echo "🎉 Setup complete! Starting the API server..."
echo "📍 API will be available at: http://localhost:8080"
echo "📖 Visit http://localhost:8080/ for documentation"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Start the server
python run.py