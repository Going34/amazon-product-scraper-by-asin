@echo off
REM Amazon Product Scraper API - Quick Start Script for Windows
REM This script will set up and run the API automatically

echo 🚀 Amazon Product Scraper API - Quick Start
echo ===========================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Check if we're in the right directory
if not exist "app.py" (
    echo ❌ Please run this script from the amazon-product-scraper-by-asin directory
    pause
    exit /b 1
)

REM Install uv if not present
uv --version >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing uv package manager...
    python -m pip install uv
)

echo ✅ uv package manager ready

REM Create virtual environment
echo 🔧 Setting up virtual environment...
uv venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies
echo 📦 Installing dependencies...
uv pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo ⚙️ Creating environment configuration...
    (
        echo # Server Configuration
        echo PORT=8080
        echo FLASK_DEBUG=True
        echo.
        echo # Rate Limiting ^(use memory for development^)
        echo REDIS_URL=memory://
        echo.
        echo # Scraping Configuration
        echo REQUEST_DELAY=2
        echo MAX_RETRIES=3
        echo TIMEOUT=10
    ) > .env
    echo ✅ Environment file created
) else (
    echo ✅ Environment file already exists
)

REM Run tests to verify everything works
echo 🧪 Running tests to verify setup...
python -m pytest tests/ -v --tb=short

echo.
echo 🎉 Setup complete! Starting the API server...
echo 📍 API will be available at: http://localhost:8080
echo 📖 Visit http://localhost:8080/ for documentation
echo 🛑 Press Ctrl+C to stop the server
echo.

REM Start the server
python run.py

pause