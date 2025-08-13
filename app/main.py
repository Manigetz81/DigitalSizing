"""
Flask Web Application for Digital Sizing
"""

import os
import sys
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
import cv2
import numpy as np
from typing import Dict, Any, Optional
import logging

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(__file__))

from models.body_detector import BodyDetector
from models.measurement import MeasurementCalculator
from models.size_predictor import SizePredictor
from utils.image_processor import ImageProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Configure upload folder for Azure App Service
if os.environ.get('AZURE_CLIENT_ID'):  # Running on Azure
    app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
else:  # Running locally
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'uploads')

app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# Initialize components
body_detector = BodyDetector()
measurement_calculator = MeasurementCalculator()
size_predictor = SizePredictor()
image_processor = ImageProcessor()

def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index() -> str:
    """Home page with upload form."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file() -> str:
    """Handle file upload and processing."""
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        try:
            # Save uploaded file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Process the image
            results = process_image(filepath)

            return render_template('results.html',
                                 filename=filename,
                                 measurements=results['measurements'],
                                 size_recommendations=results['size_recommendations'],
                                 confidence=results['confidence'])

        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            flash(f'Error processing image: {str(e)}')
            return redirect(url_for('index'))

    flash('Invalid file type. Please upload an image file.')
    return redirect(url_for('index'))

@app.route('/api/analyze', methods=['POST'])
def api_analyze() -> Dict[str, Any]:
    """API endpoint for image analysis."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    try:
        # Save temporary file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Process the image
        results = process_image(filepath)

        # Clean up temporary file
        os.remove(filepath)

        return jsonify(results)

    except Exception as e:
        logger.error(f"API error: {str(e)}")
        return jsonify({'error': str(e)}), 500

def process_image(image_path: str) -> Dict[str, Any]:
    """
    Process an image to extract body measurements and size recommendations.

    Args:
        image_path: Path to the image file

    Returns:
        Dictionary containing measurements, size recommendations, and confidence scores
    """
    try:
        # Load and preprocess image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not load image")

        processed_image = image_processor.preprocess(image)

        # Detect body landmarks
        landmarks = body_detector.detect_landmarks(processed_image)
        if not landmarks:
            raise ValueError("No person detected in image")

        # Calculate measurements
        measurements = measurement_calculator.calculate_measurements(landmarks, processed_image.shape)

        # Get size recommendations
        size_recommendations = size_predictor.predict_sizes(measurements)

        # Calculate overall confidence
        confidence = body_detector.get_confidence_score()

        return {
            'measurements': measurements,
            'size_recommendations': size_recommendations,
            'confidence': confidence,
            'status': 'success'
        }

    except Exception as e:
        logger.error(f"Image processing error: {str(e)}")
        raise

def create_upload_folder() -> None:
    """Create upload folder if it doesn't exist."""
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

if __name__ == '__main__':
    create_upload_folder()
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)
