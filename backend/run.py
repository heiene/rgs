#!/usr/bin/env python3
"""
Flask application entry point
"""
import os
from app import create_app

# Create Flask app instance
app = create_app(os.getenv('FLASK_CONFIG') or 'development')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 