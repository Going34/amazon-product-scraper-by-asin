# 🚀 Complete Setup Guide - Amazon Product Scraper API

## 📋 What You'll Get

A fully functional Amazon Product Scraper API that:
- ✅ Accepts ASIN product IDs as input
- ✅ Returns comprehensive product details in JSON format
- ✅ Includes anti-detection measures and rate limiting
- ✅ Handles errors gracefully
- ✅ Works with the ASIN you provided: **B0DYGBSM4D**

## 🎯 Quick Start (Choose Your Method)

### Method 1: Automated Setup (Easiest)

**For Linux/macOS:**
```bash
git clone https://github.com/Going34/amazon-product-scraper-by-asin.git
cd amazon-product-scraper-by-asin
chmod +x quick_start.sh
./quick_start.sh
```

**For Windows:**
```cmd
git clone https://github.com/Going34/amazon-product-scraper-by-asin.git
cd amazon-product-scraper-by-asin
quick_start.bat
```

### Method 2: Manual Setup (Step by Step)

#### Step 1: Prerequisites
- Python 3.8+ installed
- Git installed

#### Step 2: Clone Repository
```bash
git clone https://github.com/Going34/amazon-product-scraper-by-asin.git
cd amazon-product-scraper-by-asin
```

#### Step 3: Install uv Package Manager
```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Alternative (any OS)
pip install uv
```

#### Step 4: Setup Environment
```bash
# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# OR
.venv\Scripts\activate     # Windows
```

#### Step 5: Install Dependencies
```bash
uv pip install -r requirements.txt
```

#### Step 6: Configure Environment
```bash
# Copy environment template
cp .env.example .env

# The default settings work for development
# No need to edit unless you want to change ports
```

#### Step 7: Start the API
```bash
python run.py
```

## 🧪 Test Your API

Once the server is running, test it with your ASIN:

### 1. Check API Documentation
```bash
curl http://localhost:8080/
```

### 2. Health Check
```bash
curl http://localhost:8080/health
```

### 3. Test Product Scraping (Your ASIN)
```bash
# GET method
curl http://localhost:8080/product/B0DYGBSM4D

# POST method
curl -X POST http://localhost:8080/product \
  -H "Content-Type: application/json" \
  -d '{"asin": "B0DYGBSM4D"}'
```

### 4. Test in Browser
Open your browser and visit:
- http://localhost:8080/ (API documentation)
- http://localhost:8080/health (Health check)
- http://localhost:8080/product/B0DYGBSM4D (Product data)

## 📊 Expected Results

### ✅ Success Response (if scraping works):
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

### ⚠️ Expected Response (Amazon blocking):
```json
{
  "success": false,
  "error": "Failed to fetch product page after multiple retries.",
  "error_code": "REQUEST_FAILED"
}
```

**Note:** Amazon actively blocks automated scraping, so you may see the error response. This is normal and shows the error handling is working correctly.

## 🔧 Troubleshooting

### Issue: Port Already in Use
```bash
# Change port in .env file or run with different port
PORT=9000 python run.py
```

### Issue: uv Installation Failed
```bash
# Use pip instead
pip install uv
# Or install dependencies directly
pip install -r requirements.txt
```

### Issue: Virtual Environment Problems
```bash
# Remove and recreate
rm -rf .venv
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# OR
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Issue: Permission Denied (Linux/macOS)
```bash
chmod +x quick_start.sh
```

## 🐳 Alternative: Docker Setup

If you prefer Docker:

```bash
# Build and run with Docker Compose
docker-compose up --build

# The API will be available at http://localhost:8080
```

## 📁 Project Files Overview

```
amazon-product-scraper-by-asin/
├── app.py                    # Main API application
├── run.py                    # Development server
├── requirements.txt          # Dependencies
├── .env.example             # Environment template
├── quick_start.sh           # Linux/macOS setup script
├── quick_start.bat          # Windows setup script
├── demo.py                  # Test script
├── docker-compose.yml       # Docker setup
├── tests/                   # Test suite
└── README.md                # Documentation
```

## 🎯 What Each File Does

- **app.py**: The main Flask API with all endpoints and scraping logic
- **run.py**: Simple script to start the development server
- **requirements.txt**: All Python packages needed
- **.env**: Configuration file (created from .env.example)
- **quick_start.sh/.bat**: Automated setup scripts
- **demo.py**: Test script to verify API functionality

## 🚀 Production Deployment

For production use:

1. **Use Gunicorn:**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8080 app:app
   ```

2. **Set up Redis** (for rate limiting):
   ```bash
   # Install Redis
   # Update .env file:
   REDIS_URL=redis://localhost:6379/0
   ```

3. **Use reverse proxy** (Nginx recommended)

## 📞 Support

If you encounter issues:

1. **Check the logs** in your terminal where you started the server
2. **Verify Python version**: `python --version` (should be 3.8+)
3. **Check if all dependencies installed**: `pip list`
4. **Try the demo script**: `python demo.py`
5. **Review the troubleshooting section above**

## 🎉 Success Indicators

You'll know everything is working when:

1. ✅ Server starts without errors
2. ✅ `curl http://localhost:8080/` returns API documentation
3. ✅ `curl http://localhost:8080/health` returns `{"status": "healthy"}`
4. ✅ Product endpoint returns either data or proper error message
5. ✅ All tests pass: `python -m pytest tests/ -v`

## 📖 Additional Resources

- **[README.md](README.md)** - Complete project documentation
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Detailed API reference
- **[SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)** - Extended setup guide
- **[tests/test_api.py](tests/test_api.py)** - Usage examples

---

**🎯 Your API will be ready at: http://localhost:8080**

**🧪 Test with your ASIN: http://localhost:8080/product/B0DYGBSM4D**

**Happy Scraping! 🎉**