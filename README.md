# Amazon Product Scraper API

A production-ready RESTful API service for scraping Amazon product information by ASIN (Amazon Standard Identification Number). This API provides comprehensive product details including pricing, availability, images, ratings, and specifications while implementing robust anti-detection measures and rate limiting.

## Features

- **RESTful API**: Clean endpoints for product data retrieval
- **ASIN Validation**: Proper validation of Amazon Standard Identification Numbers
- **Anti-Detection**: User-agent rotation, request delays, and retry logic
- **Rate Limiting**: Built-in rate limiting to prevent abuse
- **Error Handling**: Comprehensive error handling with proper HTTP status codes
- **Data Extraction**: Extracts title, price, availability, images, ratings, reviews, and specifications
- **Production Ready**: Docker support, logging, health checks, and monitoring
- **Security**: Input validation, secure headers, and error message sanitization

## Quick Start

### Using uv (Recommended)

1. **Install uv** (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Clone and setup**:
```bash
git clone <repository-url>
cd amazon-product-scraper-by-asin
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

3. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Run the API**:
```bash
python run.py
```

### Using Docker

```bash
docker-compose up -d
```

## API Documentation

### Base URL
```
http://localhost:12000
```

### Endpoints

#### GET /
Returns API documentation and usage information.

**Response:**
```json
{
  "name": "Amazon Product Scraper API",
  "version": "1.0.0",
  "description": "RESTful API for scraping Amazon product information by ASIN",
  "endpoints": {...},
  "rate_limits": {...}
}
```

#### GET /health
Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": 1234567890
}
```

#### GET /product/{asin}
Retrieve product information by ASIN via URL parameter.

**Parameters:**
- `asin` (string): 10-character Amazon Standard Identification Number

**Example:**
```bash
curl http://localhost:12000/product/B08N5WRWNW
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "asin": "B08N5WRWNW",
    "title": "Echo Dot (4th Gen) | Smart speaker with Alexa | Charcoal",
    "price": "$49.99",
    "availability": "In Stock",
    "images": [
      "https://m.media-amazon.com/images/I/714Rq4k05UL._AC_SL1500_.jpg"
    ],
    "description": null,
    "rating": 4.7,
    "review_count": "284,516",
    "seller": "Amazon.com",
    "specifications": {
      "Brand": "Amazon",
      "Connectivity Technology": "Wi-Fi",
      "Special Feature": "Voice Control"
    },
    "features": [
      "Meet Echo Dot - Our most popular smart speaker with a fabric design.",
      "Ready to help - Ask Alexa to play music, answer questions, play the news..."
    ]
  },
  "scraped_at": 1234567890
}
```

#### POST /product
Retrieve product information by ASIN via JSON body.

**Request Body:**
```json
{
  "asin": "B08N5WRWNW"
}
```

**Example:**
```bash
curl -X POST http://localhost:12000/product \
  -H "Content-Type: application/json" \
  -d '{"asin": "B08N5WRWNW"}'
```

### Error Responses

#### Invalid ASIN (400)
```json
{
  "success": false,
  "error": "Invalid ASIN format. ASIN must be 10 alphanumeric characters.",
  "error_code": "INVALID_ASIN"
}
```

#### Product Not Found (404)
```json
{
  "success": false,
  "error": "Product not found or no longer available.",
  "error_code": "PRODUCT_NOT_FOUND"
}
```

#### Rate Limit Exceeded (429)
```json
{
  "success": false,
  "error": "Rate limit exceeded. Please try again later.",
  "error_code": "RATE_LIMIT_EXCEEDED",
  "retry_after": 60
}
```

#### Service Unavailable (503)
```json
{
  "success": false,
  "error": "Failed to fetch product page after multiple retries.",
  "error_code": "REQUEST_FAILED"
}
```

## Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# Rate Limiting Configuration
REDIS_URL=redis://localhost:6379/0
RATE_LIMIT_STORAGE_URL=redis://localhost:6379/0

# Scraping Configuration
REQUEST_DELAY_MIN=1
REQUEST_DELAY_MAX=3
MAX_RETRIES=3
TIMEOUT=30

# Security
SECRET_KEY=your-secret-key-here
```

### Rate Limiting

Default rate limits:
- **Global**: 100 requests per hour, 20 requests per minute
- **Product endpoints**: 10 requests per minute

Rate limiting uses Redis for distributed environments or in-memory storage for development.

## Anti-Detection Features

1. **User-Agent Rotation**: Random user agents for each request
2. **Request Delays**: Configurable delays between requests (1-3 seconds default)
3. **Retry Logic**: Automatic retries with exponential backoff
4. **Session Management**: Persistent sessions with proper headers
5. **Blocking Detection**: Automatic detection of CAPTCHA and blocking responses

## Development

### Setup Development Environment

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install -e ".[dev]"

# Copy environment file
cp .env.example .env
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=app

# Run specific test
uv run pytest tests/test_api.py::test_home_endpoint
```

### Code Quality

```bash
# Format code
uv run black .

# Lint code
uv run flake8

# Type checking
uv run mypy app.py
```

## Deployment

### Docker Deployment

1. **Build and run with Docker Compose**:
```bash
docker-compose up -d
```

2. **Scale the service**:
```bash
docker-compose up -d --scale api=3
```

### Production Considerations

1. **Redis**: Use Redis for rate limiting in production
2. **Load Balancer**: Use nginx or similar for load balancing
3. **Monitoring**: Implement proper logging and monitoring
4. **Security**: Use HTTPS, secure headers, and input validation
5. **Rate Limiting**: Adjust rate limits based on your needs
6. **Proxies**: Consider using rotating proxies for high-volume scraping

## Legal and Ethical Considerations

- This API scrapes publicly available data from Amazon product pages
- Respect Amazon's robots.txt and terms of service
- Implement appropriate rate limiting to avoid overloading servers
- Use the data responsibly and in compliance with applicable laws
- Consider Amazon's Product Advertising API for commercial use

## Troubleshooting

### Common Issues

1. **Rate Limited**: Reduce request frequency or implement proxy rotation
2. **CAPTCHA Challenges**: Implement CAPTCHA solving or reduce request rate
3. **IP Blocking**: Use proxy rotation or VPN
4. **Product Not Found**: Verify ASIN format and product availability
5. **Connection Errors**: Check network connectivity and timeout settings

### Debugging

Enable debug logging:
```bash
export FLASK_DEBUG=True
python run.py
```

Check logs for detailed error information and request/response details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review existing GitHub issues
3. Create a new issue with detailed information

## Changelog

### v1.0.0
- Initial release
- RESTful API with ASIN-based product scraping
- Rate limiting and anti-detection measures
- Comprehensive error handling
- Docker support
- Full test suite
