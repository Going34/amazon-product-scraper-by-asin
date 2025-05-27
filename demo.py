#!/usr/bin/env python3
"""
Demo script to test the Amazon Product Scraper API
"""

import requests
import json
import time

def test_api(base_url="http://localhost:8080"):
    """Test the API endpoints"""
    
    print("🚀 Testing Amazon Product Scraper API")
    print("=" * 50)
    
    # Test 1: Root endpoint
    print("\n1. Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"API Name: {data['name']}")
            print(f"Version: {data['version']}")
            print("✅ Root endpoint working")
        else:
            print("❌ Root endpoint failed")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Health endpoint
    print("\n2. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Health Status: {data['status']}")
            print("✅ Health endpoint working")
        else:
            print("❌ Health endpoint failed")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Invalid ASIN validation
    print("\n3. Testing ASIN validation...")
    try:
        response = requests.get(f"{base_url}/product/invalid")
        print(f"Status: {response.status_code}")
        if response.status_code == 400:
            data = response.json()
            print(f"Error: {data['error']}")
            print("✅ ASIN validation working")
        else:
            print("❌ ASIN validation failed")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Product scraping with provided ASIN
    print("\n4. Testing product scraping with ASIN: B0DYGBSM4D...")
    try:
        response = requests.get(f"{base_url}/product/B0DYGBSM4D", timeout=30)
        print(f"Status: {response.status_code}")
        data = response.json()
        
        if data.get('success'):
            product = data['data']
            print("✅ Product scraped successfully!")
            print(f"Title: {product.get('title', 'N/A')}")
            print(f"Price: {product.get('price', 'N/A')}")
            print(f"Availability: {product.get('availability', 'N/A')}")
            print(f"Rating: {product.get('rating', 'N/A')}")
        else:
            print(f"⚠️  Scraping blocked (expected): {data.get('error')}")
            print("This is normal - Amazon blocks automated requests")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 5: POST endpoint
    print("\n5. Testing POST endpoint...")
    try:
        response = requests.post(
            f"{base_url}/product",
            json={"asin": "B0DYGBSM4D"},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        
        if data.get('success'):
            print("✅ POST endpoint working - product scraped!")
        else:
            print(f"⚠️  POST endpoint working - scraping blocked: {data.get('error')}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 API Testing Complete!")
    print(f"📍 API is running at: {base_url}")
    print("📖 Visit the root endpoint for full documentation")

if __name__ == "__main__":
    test_api()