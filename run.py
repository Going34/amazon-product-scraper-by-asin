#!/usr/bin/env python3
"""
Development server runner for Amazon Product Scraper API
"""

import os
from app import app

if __name__ == '__main__':
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Run development server
    port = int(os.getenv('PORT', 12001))
    print(f"Starting server on port {port}")
    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    )