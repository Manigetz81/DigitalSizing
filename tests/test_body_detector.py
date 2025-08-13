"""
Tests for Body Detector module.
"""

import unittest
import numpy as np
import cv2
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from models.body_detector import BodyDetector

class TestBodyDetector(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.detector = BodyDetector()

        # Create a simple test image (black image with white rectangle representing a person)
        self.test_image = np.zeros((480, 640, 3), dtype=np.uint8)
        # Add a simple "person" shape
        cv2.rectangle(self.test_image, (250, 100), (390, 450), (255, 255, 255), -1)

    def test_detector_initialization(self):
        """Test that the detector initializes correctly."""
        self.assertIsNotNone(self.detector.mp_pose)
        self.assertIsNotNone(self.detector.pose)
        self.assertEqual(self.detector._last_confidence, 0.0)

    def test_detect_landmarks_invalid_input(self):
        """Test landmark detection with invalid input."""
        # Test with None input
        result = self.detector.detect_landmarks(None)
        self.assertIsNone(result)

        # Test with empty array
        empty_image = np.array([])
        result = self.detector.detect_landmarks(empty_image)
        self.assertIsNone(result)

    def test_detect_landmarks_valid_image(self):
        """Test landmark detection with a valid image."""
        # Note: This test might not detect landmarks in a synthetic image
        # In a real test, you would use actual human photos
        result = self.detector.detect_landmarks(self.test_image)

        # The result might be None for synthetic images, which is expected
        if result is not None:
            self.assertIsInstance(result, dict)
            # Check that coordinates are within image bounds
            height, width = self.test_image.shape[:2]
            for landmark_name, (x, y) in result.items():
                self.assertGreaterEqual(x, 0)
                self.assertLess(x, width)
                self.assertGreaterEqual(y, 0)
                self.assertLess(y, height)

    def test_get_confidence_score(self):
        """Test confidence score retrieval."""
        # Initial confidence should be 0.0
        confidence = self.detector.get_confidence_score()
        self.assertEqual(confidence, 0.0)

        # After processing an image, confidence might change
        self.detector.detect_landmarks(self.test_image)
        confidence = self.detector.get_confidence_score()
        self.assertGreaterEqual(confidence, 0.0)
        self.assertLessEqual(confidence, 1.0)

    def test_get_key_landmarks(self):
        """Test key landmark extraction."""
        # Create mock landmarks
        mock_landmarks = {
            'NOSE': (320, 100),
            'LEFT_SHOULDER': (280, 150),
            'RIGHT_SHOULDER': (360, 150),
            'LEFT_HIP': (290, 300),
            'RIGHT_HIP': (350, 300),
            'LEFT_KNEE': (285, 400),
            'RIGHT_KNEE': (355, 400),
            'EXTRA_LANDMARK': (100, 100)  # This should not be in key landmarks
        }

        key_landmarks = self.detector.get_key_landmarks(mock_landmarks)

        # Check that key landmarks are present
        expected_keys = ['NOSE', 'LEFT_SHOULDER', 'RIGHT_SHOULDER', 'LEFT_HIP', 'RIGHT_HIP']
        for key in expected_keys:
            self.assertIn(key, key_landmarks)

        # Check that extra landmark is not included
        self.assertNotIn('EXTRA_LANDMARK', key_landmarks)

    def test_validate_pose(self):
        """Test pose validation."""
        # Valid pose with required landmarks
        valid_landmarks = {
            'LEFT_SHOULDER': (280, 150),
            'RIGHT_SHOULDER': (360, 150),
            'LEFT_HIP': (290, 300),
            'RIGHT_HIP': (350, 300)
        }

        self.assertTrue(self.detector.validate_pose(valid_landmarks))

        # Invalid pose - missing required landmarks
        invalid_landmarks = {
            'LEFT_SHOULDER': (280, 150),
            'RIGHT_SHOULDER': (360, 150)
            # Missing hip landmarks
        }

        self.assertFalse(self.detector.validate_pose(invalid_landmarks))

        # Invalid pose - person tilted (shoulders not horizontal)
        tilted_landmarks = {
            'LEFT_SHOULDER': (280, 150),
            'RIGHT_SHOULDER': (360, 200),  # Significant Y difference
            'LEFT_HIP': (290, 300),
            'RIGHT_HIP': (350, 300)
        }

        self.assertFalse(self.detector.validate_pose(tilted_landmarks))

    def test_draw_landmarks(self):
        """Test landmark drawing functionality."""
        landmarks = {
            'NOSE': (320, 100),
            'LEFT_SHOULDER': (280, 150),
            'RIGHT_SHOULDER': (360, 150)
        }

        annotated_image = self.detector.draw_landmarks(self.test_image, landmarks)

        # Check that the annotated image has the same shape as the original
        self.assertEqual(annotated_image.shape, self.test_image.shape)

        # Check that the image was modified (not identical to original)
        self.assertFalse(np.array_equal(annotated_image, self.test_image))

if __name__ == '__main__':
    unittest.main()
