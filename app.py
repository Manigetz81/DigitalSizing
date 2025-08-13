import os
import sys
from pathlib import Path

# Ensure we can import our modules
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir / 'app'))

# Import the Flask application
try:
    from app.main import app, create_upload_folder
    print("Successfully imported Flask app from app.main")
except ImportError as e:
    print(f"Failed to import from app.main: {e}")
    # Fallback import
    sys.path.insert(0, str(current_dir / 'app'))
    from main import app, create_upload_folder
    print("Successfully imported Flask app from main")

# Ensure upload folder exists
try:
    create_upload_folder()
    print("Upload folder created/verified")
except Exception as e:
    print(f"Warning: Could not create upload folder: {e}")

# Configure for production
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-secret-key-for-azure')
app.config['DEBUG'] = False

# WSGI callable
application = app

if __name__ == "__main__":
    # For local testing
    port = int(os.environ.get('PORT', 8000))
    print(f"Starting app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
