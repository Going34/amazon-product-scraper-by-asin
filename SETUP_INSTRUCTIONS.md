# 🚀 Amazon Product Scraper API - Local Setup Instructions

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.8+** (Python 3.9 or higher recommended)
- **Git** (for cloning the repository)
- **uv** (Python package manager - we'll install this)

## Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/Going34/amazon-product-scraper-by-asin.git

# Navigate to the project directory
cd amazon-product-scraper-by-asin
```

## Step 2: Install uv Package Manager

### On macOS/Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### On Windows (PowerShell):
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Alternative: Install via pip
```bash
pip install uv
```

## Step 3: Set Up Python Environment

```bash
# Create a virtual environment
uv venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

## Step 4: Install Dependencies

```bash
# Install all required packages
uv pip install -r requirements.txt
```

## Step 5: Configure Environment

```bash
# Copy the environment template
cp .env.example .env

# Edit the .env file (optional - defaults work for development)
# You can use any text editor like nano, vim, or VS Code
nano .env
```

### Environment Configuration (.env file):
```bash
# Server Configuration
PORT=8080
FLASK_DEBUG=True

# Rate Limiting (use memory for development, Redis for production)
REDIS_URL=memory://

# Scraping Configuration
REQUEST_DELAY=2
MAX_RETRIES=3
TIMEOUT=10
```

## Step 6: Run the API Server

### Development Server (Recommended for testing):
```bash
python run.py
```

### Production Server (using Gunicorn):
```bash
# Install gunicorn if not already installed
uv pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:8080 app:app
```

## Step 7: Test the API

### Option 1: Using curl
```bash
# Test root endpoint
curl http://localhost:8080/

# Test health check
curl http://localhost:8080/health

# Test product scraping with your ASIN
curl http://localhost:8080/product/B0DYGBSM4D

# Test POST endpoint
curl -X POST http://localhost:8080/product \
  -H "Content-Type: application/json" \
  -d '{"asin": "B0DYGBSM4D"}'
```

### Option 2: Using the demo script
```bash
python demo.py
```

### Option 3: Using your web browser
Open your browser and visit:
- http://localhost:8080/ (API documentation)
- http://localhost:8080/health (Health check)
- http://localhost:8080/product/B0DYGBSM4D (Product scraping)

## Step 8: Run Tests (Optional)

```bash
# Run the test suite
python -m pytest tests/ -v

# Run tests with coverage
python -m pytest tests/ --cov=app --cov-report=html
```

## 🐳 Alternative: Docker Setup

If you prefer using Docker:

### Prerequisites for Docker:
- Docker installed on your system
- Docker Compose (usually comes with Docker)

### Docker Commands:
```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build manually
docker build -t amazon-scraper-api .
docker run -p 8080:8080 amazon-scraper-api
```

## 📋 API Usage Examples

### 1. Get API Documentation
```bash
curl http://localhost:8080/
```

### 2. Health Check
```bash
curl http://localhost:8080/health
```

### 3. Scrape Product by ASIN (GET)
```bash
curl http://localhost:8080/product/B0DYGBSM4D
```

### 4. Scrape Product by ASIN (POST)
```bash
curl -X POST http://localhost:8080/product \
  -H "Content-Type: application/json" \
  -d '{"asin": "B0DYGBSM4D"}'
```

### 5. Test with Invalid ASIN (should return error)
```bash
curl http://localhost:8080/product/invalid123
```

## 📊 Expected Response Format

### Success Response:
```json
{
  "success": true,
  "data": {
    "asin": "B0DYGBSM4D",
    "title": "Product Title",
    "price": "$29.99",
    "availability": "In Stock",
    "rating": 4.5,
    "review_count": "1,234",
    "seller": "Amazon.com",
    "images": ["image_url_1", "image_url_2"],
    "features": ["Feature 1", "Feature 2"],
    "specifications": {"Brand": "Example"},
    "description": "Product description..."
  },
  "scraped_at": 1234567890
}
```

### Error Response:
```json
{
  "success": false,
  "error": "Error description",
  "error_code": "ERROR_CODE"
}
```

## 🚨 Important Notes

### Amazon Anti-Bot Detection
- Amazon actively blocks automated scraping attempts
- The API includes retry mechanisms and anti-detection measures
- You may see "REQUEST_FAILED" errors - this is expected behavior
- For production use, consider using proxy services

### Rate Limiting
- Default: 100 requests per hour, 20 requests per minute
- Uses memory storage in development
- For production, configure Redis for distributed rate limiting

### Security Considerations
- Only scrapes publicly available data
- Implements proper error handling
- Includes input validation and sanitization

## 🔧 Troubleshooting

### Common Issues:

1. **Port already in use:**
   ```bash
   # Change port in .env file or run with different port
   PORT=9000 python run.py
   ```

2. **Permission denied on uv installation:**
   ```bash
   # Try installing with pip instead
   pip install uv
   ```

3. **Virtual environment activation issues:**
   ```bash
   # Make sure you're in the project directory
   cd amazon-product-scraper-by-asin
   
   # Try creating a new virtual environment
   rm -rf .venv
   uv venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   ```

4. **Dependencies installation fails:**
   ```bash
   # Try installing with pip
   pip install -r requirements.txt
   ```

5. **API returns 503 errors:**
   - This is expected - Amazon blocks automated requests
   - The error handling is working correctly
   - Try different ASINs or implement proxy rotation for production

### Getting Help:
- Check the logs in the terminal where you started the server
- Review the test suite for usage examples
- Ensure all dependencies are properly installed
- Verify Python version compatibility (3.8+)

## 📁 Project Structure

```
amazon-product-scraper-by-asin/
├── app.py                 # Main Flask application
├── run.py                 # Development server runner
├── requirements.txt       # Python dependencies
├── pyproject.toml        # Project configuration
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── .env                  # Environment variables
├── .env.example          # Environment template
├── tests/                # Test suite
│   └── test_api.py
├── demo.py               # API demonstration script
├── README.md             # Project documentation
├── API_DOCUMENTATION.md  # Detailed API docs
└── SETUP_INSTRUCTIONS.md # This file
```

## 🎯 Next Steps

1. **Start the server:** `python run.py`
2. **Test the API:** Visit http://localhost:8080/
3. **Try scraping:** Use ASIN "B0DYGBSM4D" for testing
4. **Read the docs:** Check API_DOCUMENTATION.md for detailed usage
5. **Run tests:** Execute `python -m pytest tests/ -v`

## 🚀 Production Deployment

For production deployment:
1. Use Gunicorn or uWSGI as WSGI server
2. Set up Redis for rate limiting
3. Configure reverse proxy (Nginx)
4. Implement proper logging and monitoring
5. Consider proxy rotation for high-volume scraping

---

**Happy Scraping! 🎉**

If you encounter any issues, check the troubleshooting section or review the logs for detailed error information.