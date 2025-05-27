"""
Test suite for Amazon Product Scraper API
"""

import pytest
import json
from app import app, scraper


@pytest.fixture
def client():
    """Create test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_endpoint(client):
    """Test the home/documentation endpoint."""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Amazon Product Scraper API'
    assert 'endpoints' in data


def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'timestamp' in data


def test_product_endpoint_invalid_asin(client):
    """Test product endpoint with invalid ASIN."""
    response = client.get('/product/INVALID')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert data['error_code'] == 'INVALID_ASIN'


def test_product_endpoint_valid_format(client):
    """Test product endpoint with valid ASIN format."""
    # Using a test ASIN - this might fail if the product doesn't exist
    response = client.get('/product/B08N5WRWNW')
    data = json.loads(response.data)
    
    # Should either succeed or fail with a specific error
    assert 'success' in data
    if not data['success']:
        assert 'error_code' in data


def test_product_post_endpoint_missing_asin(client):
    """Test POST product endpoint with missing ASIN."""
    response = client.post('/product', 
                          data=json.dumps({}),
                          content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert data['error_code'] == 'MISSING_ASIN'


def test_product_post_endpoint_valid_asin(client):
    """Test POST product endpoint with valid ASIN."""
    response = client.post('/product',
                          data=json.dumps({'asin': 'B08N5WRWNW'}),
                          content_type='application/json')
    data = json.loads(response.data)
    assert 'success' in data


def test_asin_validation():
    """Test ASIN validation function."""
    assert scraper._validate_asin('B08N5WRWNW') is True
    assert scraper._validate_asin('INVALID') is False
    assert scraper._validate_asin('') is False
    assert scraper._validate_asin('B08N5WRWN') is False  # Too short
    assert scraper._validate_asin('B08N5WRWNW1') is False  # Too long


def test_price_cleaning():
    """Test price cleaning function."""
    assert scraper._clean_price('$29.99') == '$29.99'
    assert scraper._clean_price('Price: $29.99') == '$29.99'
    assert scraper._clean_price('') is None
    assert scraper._clean_price(None) is None


def test_404_handler(client):
    """Test 404 error handler."""
    response = client.get('/nonexistent')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['success'] is False
    assert data['error_code'] == 'ENDPOINT_NOT_FOUND'