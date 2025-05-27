"""
Amazon Product Scraper API

A RESTful API service for scraping Amazon product information by ASIN.
Includes rate limiting, error handling, and anti-detection measures.
"""

import os
import re
import time
import random
import logging
from typing import Dict, Any, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Initialize rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=os.getenv('RATE_LIMIT_STORAGE_URL', 'memory://'),
    default_limits=["100 per hour", "20 per minute"]
)
limiter.init_app(app)

class AmazonScraper:
    """Amazon product scraper with anti-detection measures."""
    
    def __init__(self):
        self.session = requests.Session()
        self.ua = UserAgent()
        self.base_url = "https://www.amazon.com"
        self.request_delay_min = int(os.getenv('REQUEST_DELAY_MIN', 1))
        self.request_delay_max = int(os.getenv('REQUEST_DELAY_MAX', 3))
        self.max_retries = int(os.getenv('MAX_RETRIES', 3))
        self.timeout = int(os.getenv('TIMEOUT', 30))
        
        # Setup session headers
        self._setup_session()
        
    def _setup_session(self):
        """Configure session with headers and settings."""
        self.session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
    def _get_random_headers(self) -> Dict[str, str]:
        """Generate random headers for each request."""
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def _validate_asin(self, asin: str) -> bool:
        """Validate ASIN format."""
        if not asin or len(asin) != 10:
            return False
        return bool(re.match(r'^[A-Z0-9]{10}$', asin.upper()))
    
    def _make_request(self, url: str, retries: int = 0) -> Optional[requests.Response]:
        """Make HTTP request with retry logic and anti-detection measures."""
        if retries >= self.max_retries:
            logger.error(f"Max retries exceeded for URL: {url}")
            return None
            
        try:
            # Random delay between requests
            delay = random.uniform(self.request_delay_min, self.request_delay_max)
            time.sleep(delay)
            
            # Update headers for each request
            headers = self._get_random_headers()
            
            response = self.session.get(
                url,
                headers=headers,
                timeout=self.timeout,
                allow_redirects=True
            )
            
            # Check for common blocking indicators
            if self._is_blocked(response):
                logger.warning(f"Request blocked, retrying... (attempt {retries + 1})")
                return self._make_request(url, retries + 1)
                
            response.raise_for_status()
            return response
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            if retries < self.max_retries:
                return self._make_request(url, retries + 1)
            return None
    
    def _is_blocked(self, response: requests.Response) -> bool:
        """Check if the request was blocked by Amazon."""
        if response.status_code == 503:
            return True
            
        content = response.text.lower()
        blocking_indicators = [
            'captcha',
            'robot',
            'automated',
            'blocked',
            'access denied',
            'sorry, we just need to make sure you\'re not a robot'
        ]
        
        return any(indicator in content for indicator in blocking_indicators)
    
    def _extract_product_data(self, soup: BeautifulSoup, asin: str) -> Dict[str, Any]:
        """Extract product data from Amazon product page."""
        product_data = {
            'asin': asin,
            'title': None,
            'price': None,
            'availability': None,
            'images': [],
            'description': None,
            'rating': None,
            'review_count': None,
            'seller': None,
            'specifications': {},
            'features': []
        }
        
        try:
            # Extract title
            title_selectors = [
                '#productTitle',
                '.product-title',
                'h1.a-size-large'
            ]
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    product_data['title'] = title_elem.get_text(strip=True)
                    break
            
            # Extract price
            price_selectors = [
                '.a-price-whole',
                '.a-price .a-offscreen',
                '#price_inside_buybox',
                '.a-price-range'
            ]
            for selector in price_selectors:
                price_elem = soup.select_one(selector)
                if price_elem:
                    price_text = price_elem.get_text(strip=True)
                    product_data['price'] = self._clean_price(price_text)
                    break
            
            # Extract availability
            availability_selectors = [
                '#availability span',
                '.a-color-success',
                '.a-color-state'
            ]
            for selector in availability_selectors:
                avail_elem = soup.select_one(selector)
                if avail_elem:
                    product_data['availability'] = avail_elem.get_text(strip=True)
                    break
            
            # Extract images
            img_selectors = [
                '#landingImage',
                '.a-dynamic-image',
                '#imgTagWrapperId img'
            ]
            for selector in img_selectors:
                img_elem = soup.select_one(selector)
                if img_elem and img_elem.get('src'):
                    product_data['images'].append(img_elem['src'])
            
            # Extract additional images from image gallery
            gallery_imgs = soup.select('.a-button-thumbnail img')
            for img in gallery_imgs:
                if img.get('src'):
                    product_data['images'].append(img['src'])
            
            # Remove duplicates from images
            product_data['images'] = list(set(product_data['images']))
            
            # Extract description/features
            feature_bullets = soup.select('#feature-bullets ul li span')
            for bullet in feature_bullets:
                text = bullet.get_text(strip=True)
                if text and len(text) > 10:
                    product_data['features'].append(text)
            
            # Extract rating
            rating_elem = soup.select_one('.a-icon-alt')
            if rating_elem:
                rating_text = rating_elem.get_text()
                rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                if rating_match:
                    product_data['rating'] = float(rating_match.group(1))
            
            # Extract review count
            review_elem = soup.select_one('#acrCustomerReviewText')
            if review_elem:
                review_text = review_elem.get_text()
                review_match = re.search(r'([\d,]+)', review_text)
                if review_match:
                    product_data['review_count'] = review_match.group(1).replace(',', '')
            
            # Extract seller information
            seller_elem = soup.select_one('#sellerProfileTriggerId')
            if seller_elem:
                product_data['seller'] = seller_elem.get_text(strip=True)
            
            # Extract specifications from product details
            detail_bullets = soup.select('#detailBullets_feature_div ul li')
            for bullet in detail_bullets:
                spans = bullet.select('span')
                if len(spans) >= 2:
                    key = spans[0].get_text(strip=True).replace(':', '')
                    value = spans[1].get_text(strip=True)
                    if key and value:
                        product_data['specifications'][key] = value
            
        except Exception as e:
            logger.error(f"Error extracting product data: {e}")
        
        return product_data
    
    def _clean_price(self, price_text: str) -> Optional[str]:
        """Clean and format price text."""
        if not price_text:
            return None
        
        # Remove extra whitespace and common price prefixes
        price_text = re.sub(r'[^\d.,\$]', '', price_text)
        return price_text if price_text else None
    
    def scrape_product(self, asin: str) -> Dict[str, Any]:
        """Scrape product information by ASIN."""
        # Validate ASIN
        if not self._validate_asin(asin):
            return {
                'success': False,
                'error': 'Invalid ASIN format. ASIN must be 10 alphanumeric characters.',
                'error_code': 'INVALID_ASIN'
            }
        
        # Construct product URL
        product_url = f"{self.base_url}/dp/{asin.upper()}"
        
        logger.info(f"Scraping product: {asin}")
        
        # Make request
        response = self._make_request(product_url)
        if not response:
            return {
                'success': False,
                'error': 'Failed to fetch product page after multiple retries.',
                'error_code': 'REQUEST_FAILED'
            }
        
        # Parse HTML
        try:
            soup = BeautifulSoup(response.content, 'lxml')
        except Exception as e:
            logger.error(f"Failed to parse HTML: {e}")
            return {
                'success': False,
                'error': 'Failed to parse product page.',
                'error_code': 'PARSE_ERROR'
            }
        
        # Check if product exists
        if self._is_product_not_found(soup):
            return {
                'success': False,
                'error': 'Product not found or no longer available.',
                'error_code': 'PRODUCT_NOT_FOUND'
            }
        
        # Extract product data
        product_data = self._extract_product_data(soup, asin.upper())
        
        return {
            'success': True,
            'data': product_data,
            'scraped_at': time.time()
        }
    
    def _is_product_not_found(self, soup: BeautifulSoup) -> bool:
        """Check if the product page indicates the product was not found."""
        not_found_indicators = [
            'page not found',
            'looking for something',
            'we couldn\'t find that page',
            'dogs of amazon'
        ]
        
        page_text = soup.get_text().lower()
        return any(indicator in page_text for indicator in not_found_indicators)

# Initialize scraper
scraper = AmazonScraper()

@app.route('/', methods=['GET'])
def home():
    """API documentation endpoint."""
    return jsonify({
        'name': 'Amazon Product Scraper API',
        'version': '1.0.0',
        'description': 'RESTful API for scraping Amazon product information by ASIN',
        'endpoints': {
            'GET /': 'API documentation',
            'GET /health': 'Health check',
            'GET /product/<asin>': 'Get product information by ASIN',
            'POST /product': 'Get product information by ASIN (JSON body)'
        },
        'rate_limits': {
            'default': '100 requests per hour, 20 requests per minute'
        },
        'example_usage': {
            'url': '/product/B08N5WRWNW',
            'response_format': {
                'success': True,
                'data': {
                    'asin': 'B08N5WRWNW',
                    'title': 'Product Title',
                    'price': '$29.99',
                    'availability': 'In Stock',
                    'images': ['image_url_1', 'image_url_2'],
                    'description': 'Product description',
                    'rating': 4.5,
                    'review_count': '1,234',
                    'seller': 'Seller Name',
                    'specifications': {},
                    'features': []
                },
                'scraped_at': 1234567890
            }
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time()
    })

@app.route('/product/<asin>', methods=['GET'])
@limiter.limit("10 per minute")
def get_product_by_asin(asin):
    """Get product information by ASIN via URL parameter."""
    try:
        result = scraper.scrape_product(asin)
        
        if result['success']:
            return jsonify(result), 200
        else:
            # Return appropriate HTTP status codes based on error type
            status_code = 400  # Bad Request
            if result.get('error_code') == 'PRODUCT_NOT_FOUND':
                status_code = 404  # Not Found
            elif result.get('error_code') == 'REQUEST_FAILED':
                status_code = 503  # Service Unavailable
            
            return jsonify(result), status_code
            
    except Exception as e:
        logger.error(f"Unexpected error in get_product_by_asin: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error occurred.',
            'error_code': 'INTERNAL_ERROR'
        }), 500

@app.route('/product', methods=['POST'])
@limiter.limit("10 per minute")
def get_product_by_json():
    """Get product information by ASIN via JSON body."""
    try:
        data = request.get_json()
        
        if not data or 'asin' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing ASIN in request body. Expected JSON: {"asin": "B08N5WRWNW"}',
                'error_code': 'MISSING_ASIN'
            }), 400
        
        asin = data['asin']
        result = scraper.scrape_product(asin)
        
        if result['success']:
            return jsonify(result), 200
        else:
            # Return appropriate HTTP status codes based on error type
            status_code = 400  # Bad Request
            if result.get('error_code') == 'PRODUCT_NOT_FOUND':
                status_code = 404  # Not Found
            elif result.get('error_code') == 'REQUEST_FAILED':
                status_code = 503  # Service Unavailable
            
            return jsonify(result), status_code
            
    except Exception as e:
        logger.error(f"Unexpected error in get_product_by_json: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error occurred.',
            'error_code': 'INTERNAL_ERROR'
        }), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit exceeded errors."""
    return jsonify({
        'success': False,
        'error': 'Rate limit exceeded. Please try again later.',
        'error_code': 'RATE_LIMIT_EXCEEDED',
        'retry_after': e.retry_after
    }), 429

@app.errorhandler(404)
def not_found_handler(e):
    """Handle 404 errors."""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found.',
        'error_code': 'ENDPOINT_NOT_FOUND'
    }), 404

@app.errorhandler(500)
def internal_error_handler(e):
    """Handle internal server errors."""
    return jsonify({
        'success': False,
        'error': 'Internal server error occurred.',
        'error_code': 'INTERNAL_ERROR'
    }), 500

if __name__ == '__main__':
    # Configure CORS and host settings for the runtime environment
    app.run(
        host='0.0.0.0',
        port=12000,
        debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    )