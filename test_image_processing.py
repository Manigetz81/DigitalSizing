#!/usr/bin/env python3
"""
Test image processing with actual image
"""

import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

try:
    print("Testing with real image...")

    from models.body_detector import BodyDetector
    from models.measurement import MeasurementCalculator
    from models.size_predictor import SizePredictor
    from utils.image_processor import ImageProcessor
    import cv2

    # Initialize components
    body_detector = BodyDetector()
    measurement_calculator = MeasurementCalculator()
    size_predictor = SizePredictor()
    image_processor = ImageProcessor()

    # Test with actual image
    image_path = "app/static/uploads/test_image.jfif"

    if not os.path.exists(image_path):
        print(f"Test image not found at {image_path}")
        sys.exit(1)

    print(f"Loading image: {image_path}")
    image = cv2.imread(image_path)

    if image is None:
        print("Could not load image")
        sys.exit(1)

    print(f"Image loaded successfully, shape: {image.shape}")

    # Preprocess
    processed_image = image_processor.preprocess(image)
    print(f"Image preprocessed, shape: {processed_image.shape}")

    # Detect landmarks
    landmarks = body_detector.detect_landmarks(processed_image)

    if landmarks:
        print(f"✓ Landmarks detected: {len(landmarks)} points")
        for name, (x, y) in landmarks.items():
            print(f"  {name}: ({x:.1f}, {y:.1f})")

        # Calculate measurements
        measurements = measurement_calculator.calculate_measurements(landmarks, processed_image.shape)
        print(f"✓ Measurements calculated: {measurements}")

        # Get size recommendations
        size_recommendations = size_predictor.predict_sizes(measurements)
        print(f"✓ Size recommendations: {size_recommendations}")

        # Get confidence
        confidence = body_detector.get_confidence_score()
        print(f"✓ Confidence score: {confidence}")

        print("\n✅ Full pipeline works correctly!")

    else:
        print("❌ No landmarks detected")

        # Check if face detection works
        gray = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        if len(faces) > 0:
            print(f"Face detection found {len(faces)} faces")
            for i, (x, y, w, h) in enumerate(faces):
                print(f"  Face {i+1}: x={x}, y={y}, w={w}, h={h}")
        else:
            print("No faces detected by OpenCV face detection")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
