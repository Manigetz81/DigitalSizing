#!/bin/bash

# Azure App Service startup script
echo "Starting Digital Sizing Application..."

# Create necessary directories
mkdir -p /tmp/uploads
chmod 755 /tmp/uploads

# Install dependencies if needed
if [ -f requirements.txt ]; then
    echo "Installing dependencies..."
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
fi

# Start the application with gunicorn
echo "Starting Gunicorn server..."
exec gunicorn --config gunicorn.conf.py app:application
