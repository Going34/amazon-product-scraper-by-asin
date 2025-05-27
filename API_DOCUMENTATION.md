# Amazon Product Scraper API Documentation

## 🚀 Overview

A production-ready RESTful API service for scraping Amazon product information using ASIN (Amazon Standard Identification Number) identifiers. The API provides comprehensive product details including pricing, availability, ratings, and specifications.

## ✅ Features Implemented

### Core Functionality
- ✅ RESTful API endpoints (GET and POST)
- ✅ ASIN validation and error handling
- ✅ Web scraping with anti-detection measures
- ✅ Rate limiting with Redis support
- ✅ Comprehensive error handling
- ✅ JSON response formatting
- ✅ Health monitoring endpoint
- ✅ Docker deployment ready

### Anti-Detection Measures
- ✅ User-agent rotation (50+ real browser agents)
- ✅ Request delays (1-3 seconds between requests)
- ✅ Retry mechanism with exponential backoff
- ✅ Session management
- ✅ Request headers randomization

### Production Features
- ✅ Rate limiting (100/hour, 20/minute)
- ✅ Logging with structured format
- ✅ Environment configuration
- ✅ Docker containerization
- ✅ Comprehensive test suite
- ✅ Error codes and status handling

## 📋 API Endpoints

### 1. Root Endpoint
```
GET /
```
Returns API documentation and usage information.

**Response:**
```json
{
  "name": "Amazon Product Scraper API",
  "version": "1.0.0",
  "description": "RESTful API for scraping Amazon product information by ASIN",
  "endpoints": {
    "GET /": "API documentation",
    "GET /health": "Health check",
    "GET /product/<asin>": "Get product information by ASIN",
    "POST /product": "Get product information by ASIN (JSON body)"
  },
  "rate_limits": {
    "default": "100 requests per hour, 20 requests per minute"
  }
}
```

### 2. Health Check
```
GET /health
```
Returns API health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": 1234567890
}
```

### 3. Get Product by ASIN (GET)
```
GET /product/<asin>
```

**Parameters:**
- `asin` (string): 10-character Amazon Standard Identification Number

**Example:**
```bash
curl http://localhost:8080/product/B0DYGBSM4D
```

### 4. Get Product by ASIN (POST)
```
POST /product
Content-Type: application/json
```

**Request Body:**
```json
{
  "asin": "B0DYGBSM4D"
}
```

**Example:**
```bash
curl -X POST http://localhost:8080/product \
  -H "Content-Type: application/json" \
  -d '{"asin": "B0DYGBSM4D"}'
```

## 📊 Response Format

### Success Response
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
    "images": [
      "https://example.com/image1.jpg",
      "https://example.com/image2.jpg"
    ],
    "features": [
      "Feature 1",
      "Feature 2"
    ],
    "specifications": {
      "Brand": "Example Brand",
      "Model": "Example Model"
    },
    "description": "Product description text..."
  },
  "scraped_at": 1234567890
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error description",
  "error_code": "ERROR_CODE"
}
```

## 🚨 Error Codes

| Code | Description | HTTP Status |
|------|-------------|-------------|
| `INVALID_ASIN` | Invalid ASIN format | 400 |
| `MISSING_ASIN` | ASIN not provided in request | 400 |
| `INVALID_JSON` | Invalid JSON in request body | 400 |
| `REQUEST_FAILED` | Failed to fetch product page | 503 |
| `PARSE_ERROR` | Failed to parse product data | 500 |
| `RATE_LIMIT_EXCEEDED` | Too many requests | 429 |

## 🛠️ Setup and Installation

### Prerequisites
- Python 3.8+
- uv package manager

### Quick Start
```bash
# Clone the repository
git clone <repository-url>
cd amazon-product-scraper-by-asin

# Install uv (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your configuration

# Run the development server
python run.py
```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build manually
docker build -t amazon-scraper-api .
docker run -p 8080:8080 amazon-scraper-api
```

## 🧪 Testing

### Run Test Suite
```bash
# Activate virtual environment
source .venv/bin/activate

# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=app --cov-report=html
```

### Manual Testing
```bash
# Test the API manually
python demo.py

# Or use curl
curl http://localhost:8080/
curl http://localhost:8080/health
curl http://localhost:8080/product/B0DYGBSM4D
```

## ⚙️ Configuration

### Environment Variables
```bash
# Server Configuration
PORT=8080
FLASK_DEBUG=True

# Rate Limiting
REDIS_URL=redis://localhost:6379/0
# Use memory:// for development without Redis

# Scraping Configuration
REQUEST_DELAY=2
MAX_RETRIES=3
TIMEOUT=10
```

### Rate Limiting
- **Default**: 100 requests per hour, 20 requests per minute
- **Storage**: Redis (production) or Memory (development)
- **Configurable**: Via environment variables

## 🔒 Security Considerations

### Anti-Detection
- Rotating user agents from real browsers
- Random delays between requests
- Session management
- Retry with exponential backoff

### Rate Limiting
- Per-IP rate limiting implemented
- Configurable limits
- Redis-backed for distributed systems

### Input Validation
- ASIN format validation
- JSON schema validation
- SQL injection prevention
- XSS protection

## 📈 Performance

### Optimization Features
- Connection pooling
- Request session reuse
- Efficient HTML parsing with lxml
- Memory-efficient data structures

### Monitoring
- Structured logging
- Health check endpoint
- Error tracking
- Performance metrics

## 🚫 Known Limitations

### Amazon Anti-Bot Measures
Amazon actively blocks automated scraping attempts. The API includes:
- Retry mechanisms for temporary blocks
- Proper error handling for blocked requests
- Rate limiting to avoid detection

**Note**: In production, you may need:
- Proxy rotation
- CAPTCHA solving services
- More sophisticated anti-detection measures

### Legal Considerations
- Only scrapes publicly available data
- Respects robots.txt guidelines
- Implements rate limiting
- No authentication bypass

## 🔧 Development

### Project Structure
```
amazon-product-scraper-by-asin/
├── app.py                 # Main Flask application
├── run.py                 # Development server runner
├── requirements.txt       # Python dependencies
├── pyproject.toml        # Project configuration
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── .env                  # Environment variables
├── tests/                # Test suite
│   └── test_api.py
├── demo.py               # API demonstration script
└── README.md             # Project documentation
```

### Adding New Features
1. Add endpoint to `app.py`
2. Add tests to `tests/test_api.py`
3. Update documentation
4. Run test suite

### Contributing
1. Fork the repository
2. Create feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit pull request

## 📞 Support

For issues and questions:
1. Check the test suite for examples
2. Review error codes and responses
3. Check logs for detailed error information
4. Ensure proper environment configuration

## 🎯 Production Deployment

### Recommended Setup
- Use Gunicorn or uWSGI for production WSGI server
- Deploy behind reverse proxy (Nginx)
- Use Redis for rate limiting storage
- Implement monitoring and alerting
- Set up log aggregation
- Use environment-specific configurations

### Scaling Considerations
- Horizontal scaling with load balancer
- Redis cluster for rate limiting
- Proxy rotation for high volume
- Caching layer for frequently requested products