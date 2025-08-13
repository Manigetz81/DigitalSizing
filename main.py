#!/usr/bin/env python3
"""
Simple entry point for Azure App Service
"""
import os
import sys

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'app'))

# Import Flask app
from app.main import app

# Configure for Azure
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'azure-fallback-key'),
    DEBUG=False
)

# This is what Azure App Service will look for
application = app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
