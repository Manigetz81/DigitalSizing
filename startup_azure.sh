#!/bin/bash

echo "Starting Digital Sizing Application..."

# Create upload directory
mkdir -p /tmp/uploads
echo "Created upload directory"

# Set Python path
export PYTHONPATH=/home/site/wwwroot:$PYTHONPATH
echo "Python path set: $PYTHONPATH"

# Start with gunicorn
echo "Starting Gunicorn..."
cd /home/site/wwwroot
exec gunicorn --bind 0.0.0.0:8000 --timeout 120 --workers 1 app:application
