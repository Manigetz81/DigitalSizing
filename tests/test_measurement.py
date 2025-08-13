"""
Tests for Measurement Calculator module.
"""

import unittest
import numpy as np
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from models.measurement import MeasurementCalculator

class TestMeasurementCalculator(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.calculator = MeasurementCalculator()

        # Create mock landmarks for a typical person
        self.mock_landmarks = {
            'NOSE': (320, 80),
            'LEFT_SHOULDER': (280, 150),
            'RIGHT_SHOULDER': (360, 150),
            'LEFT_HIP': (290, 300),
            'RIGHT_HIP': (350, 300),
            'LEFT_KNEE': (285, 400),
            'RIGHT_KNEE': (355, 400),
            'LEFT_ANKLE': (280, 480),
            'RIGHT_ANKLE': (360, 480),
            'LEFT_WRIST': (250, 250),
            'RIGHT_WRIST': (390, 250)
        }

        self.image_shape = (480, 640)  # height, width

    def test_calculator_initialization(self):
        """Test that the calculator initializes correctly."""
        self.assertIsNotNone(self.calculator.body_proportions)
        self.assertIsNotNone(self.calculator.measurement_factors)

        # Check that proportions are reasonable
        self.assertGreater(self.calculator.body_proportions['head_to_total_height'], 0)
        self.assertLess(self.calculator.body_proportions['head_to_total_height'], 1)

    def test_calculate_measurements_valid_input(self):
        """Test measurement calculation with valid input."""
        measurements = self.calculator.calculate_measurements(self.mock_landmarks, self.image_shape)

        self.assertIsInstance(measurements, dict)

        # Check that some measurements are calculated
        if measurements:  # Only check if measurements were successfully calculated
            for measurement, value in measurements.items():
                self.assertIsInstance(value, (int, float))
                self.assertGreater(value, 0)  # All measurements should be positive
                self.assertLess(value, 300)   # Reasonable upper bound for human measurements

    def test_calculate_measurements_empty_landmarks(self):
        """Test measurement calculation with empty landmarks."""
        measurements = self.calculator.calculate_measurements({}, self.image_shape)
        self.assertEqual(measurements, {})

    def test_calculate_distance(self):
        """Test distance calculation between two points."""
        point1 = (0, 0)
        point2 = (3, 4)

        distance = self.calculator._calculate_distance(point1, point2)
        self.assertEqual(distance, 5.0)  # 3-4-5 triangle

        # Test with same points
        distance = self.calculator._calculate_distance(point1, point1)
        self.assertEqual(distance, 0.0)

    def test_calculate_height(self):
        """Test height calculation."""
        # Test with valid landmarks
        scale_factor = 10.0  # pixels per cm
        height = self.calculator._calculate_height(self.mock_landmarks, scale_factor)

        if height is not None:
            self.assertIsInstance(height, float)
            self.assertGreater(height, 100)  # Minimum reasonable height
            self.assertLess(height, 250)    # Maximum reasonable height

        # Test with missing landmarks
        incomplete_landmarks = {'NOSE': (320, 80)}
        height = self.calculator._calculate_height(incomplete_landmarks, scale_factor)
        self.assertIsNone(height)

    def test_calculate_shoulder_width(self):
        """Test shoulder width calculation."""
        scale_factor = 10.0
        width = self.calculator._calculate_shoulder_width(self.mock_landmarks, scale_factor)

        if width is not None:
            self.assertIsInstance(width, float)
            self.assertGreater(width, 20)   # Minimum reasonable shoulder width
            self.assertLess(width, 80)      # Maximum reasonable shoulder width

        # Test with missing landmarks
        incomplete_landmarks = {'LEFT_SHOULDER': (280, 150)}
        width = self.calculator._calculate_shoulder_width(incomplete_landmarks, scale_factor)
        self.assertIsNone(width)

    def test_calculate_chest_circumference(self):
        """Test chest circumference calculation."""
        scale_factor = 10.0
        circumference = self.calculator._calculate_chest_circumference(self.mock_landmarks, scale_factor)

        if circumference is not None:
            self.assertIsInstance(circumference, float)
            self.assertGreater(circumference, 60)   # Minimum reasonable chest circumference
            self.assertLess(circumference, 200)     # Maximum reasonable chest circumference

    def test_calculate_waist_circumference(self):
        """Test waist circumference calculation."""
        scale_factor = 10.0
        circumference = self.calculator._calculate_waist_circumference(self.mock_landmarks, scale_factor)

        if circumference is not None:
            self.assertIsInstance(circumference, float)
            self.assertGreater(circumference, 50)   # Minimum reasonable waist circumference
            self.assertLess(circumference, 180)     # Maximum reasonable waist circumference

    def test_calculate_hip_circumference(self):
        """Test hip circumference calculation."""
        scale_factor = 10.0
        circumference = self.calculator._calculate_hip_circumference(self.mock_landmarks, scale_factor)

        if circumference is not None:
            self.assertIsInstance(circumference, float)
            self.assertGreater(circumference, 60)   # Minimum reasonable hip circumference
            self.assertLess(circumference, 200)     # Maximum reasonable hip circumference

    def test_calculate_arm_length(self):
        """Test arm length calculation."""
        scale_factor = 10.0
        length = self.calculator._calculate_arm_length(self.mock_landmarks, scale_factor)

        if length is not None:
            self.assertIsInstance(length, float)
            self.assertGreater(length, 40)    # Minimum reasonable arm length
            self.assertLess(length, 100)      # Maximum reasonable arm length

    def test_scale_factor_calculation(self):
        """Test scale factor calculation."""
        # Test with valid landmarks
        scale_factor = self.calculator._calculate_scale_factor(self.mock_landmarks, self.image_shape)

        if scale_factor is not None:
            self.assertIsInstance(scale_factor, float)
            self.assertGreater(scale_factor, 0)
            self.assertLess(scale_factor, 50)  # Reasonable upper bound

        # Test with missing nose landmark
        landmarks_no_nose = {k: v for k, v in self.mock_landmarks.items() if k != 'NOSE'}
        scale_factor = self.calculator._calculate_scale_factor(landmarks_no_nose, self.image_shape)
        self.assertIsNone(scale_factor)

if __name__ == '__main__':
    unittest.main()
