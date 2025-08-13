#!/usr/bin/env python3
"""
Simple test to debug the Flask app startup
"""

import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

try:
    print("Testing imports...")

    from models.body_detector import BodyDetector
    print("✓ BodyDetector imported")

    from models.measurement import MeasurementCalculator
    print("✓ MeasurementCalculator imported")

    from models.size_predictor import SizePredictor
    print("✓ SizePredictor imported")

    from utils.image_processor import ImageProcessor
    print("✓ ImageProcessor imported")

    import cv2
    print("✓ OpenCV imported")

    from flask import Flask
    print("✓ Flask imported")

    print("\nTesting object creation...")

    body_detector = BodyDetector()
    print("✓ BodyDetector created")

    measurement_calculator = MeasurementCalculator()
    print("✓ MeasurementCalculator created")

    size_predictor = SizePredictor()
    print("✓ SizePredictor created")

    image_processor = ImageProcessor()
    print("✓ ImageProcessor created")

    print("\nAll components working correctly!")

    # Test a simple image processing
    print("\nTesting image processing with a test image...")
    import numpy as np

    # Create a dummy image
    test_image = np.zeros((480, 640, 3), dtype=np.uint8)
    test_image[100:200, 200:300] = [255, 255, 255]  # Add a white rectangle (face-like)

    processed = image_processor.preprocess(test_image)
    print(f"✓ Image preprocessing works, output shape: {processed.shape}")

    landmarks = body_detector.detect_landmarks(processed)
    if landmarks:
        print(f"✓ Landmark detection works, found {len(landmarks)} landmarks")
    else:
        print("⚠ No landmarks detected (expected for dummy image)")

except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
