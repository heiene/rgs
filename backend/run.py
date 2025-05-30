#!/usr/bin/env python3
"""
Flask application entry point
"""
import os
from app import create_app

# Create Flask app instance
app = create_app(os.getenv('FLASK_CONFIG') or 'development')

if __name__ == '__main__':
    port = int(os.getenv('FLASK_RUN_PORT', 5000))
    host = os.getenv('FLASK_RUN_HOST', '127.0.0.1')
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    app.run(debug=debug, host=host, port=port) 