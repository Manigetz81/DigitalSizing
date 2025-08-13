import os
import sys
from pathlib import Path

# Add the project root to Python path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(root_dir / 'app'))

# Import the Flask application
from app.main import app, create_upload_folder

# Ensure upload folder exists
create_upload_folder()

# Configure for production
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['DEBUG'] = False

# WSGI callable
application = app

if __name__ == "__main__":
    # For local testing
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
