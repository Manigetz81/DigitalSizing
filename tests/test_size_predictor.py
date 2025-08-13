"""
Tests for Size Predictor module.
"""

import unittest
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from models.size_predictor import SizePredictor

class TestSizePredictor(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.predictor = SizePredictor()

        # Mock measurements for testing
        self.mock_measurements = {
            'height': 170.0,
            'chest_circumference': 95.0,
            'waist_circumference': 80.0,
            'hip_circumference': 100.0,
            'shoulder_width': 45.0,
            'arm_length': 62.0
        }

    def test_predictor_initialization(self):
        """Test that the predictor initializes correctly."""
        self.assertIsNotNone(self.predictor.size_charts)
        self.assertIsInstance(self.predictor.confidence_threshold, float)
        self.assertGreater(self.predictor.confidence_threshold, 0)
        self.assertLessEqual(self.predictor.confidence_threshold, 1)

    def test_predict_sizes_valid_measurements(self):
        """Test size prediction with valid measurements."""
        predictions = self.predictor.predict_sizes(self.mock_measurements)

        self.assertIsInstance(predictions, dict)

        # Check that predictions contain expected categories
        expected_categories = ['tops', 'bottoms', 'dresses', 'outerwear']
        for category in expected_categories:
            if category in predictions:
                prediction = predictions[category]
                self.assertIsInstance(prediction, dict)
                self.assertIn('size', prediction)
                self.assertIn('confidence', prediction)
                self.assertIn('fit_notes', prediction)

                # Validate size format
                self.assertIn(prediction['size'], ['XS', 'S', 'M', 'L', 'XL', 'XXL'])

                # Validate confidence range
                self.assertGreaterEqual(prediction['confidence'], 0.0)
                self.assertLessEqual(prediction['confidence'], 1.0)

                # Validate fit notes
                self.assertIsInstance(prediction['fit_notes'], list)

    def test_predict_sizes_empty_measurements(self):
        """Test size prediction with empty measurements."""
        predictions = self.predictor.predict_sizes({})

        # Should return empty dict or dict with None values
        if predictions:
            for category, prediction in predictions.items():
                # All predictions should be None if measurements are insufficient
                pass

    def test_predict_top_size(self):
        """Test top size prediction."""
        prediction = self.predictor._predict_top_size(self.mock_measurements)

        if prediction is not None:
            self.assertIsInstance(prediction, dict)
            self.assertIn('size', prediction)
            self.assertIn('confidence', prediction)
            self.assertIn('fit_notes', prediction)

            # Check size validity
            self.assertIn(prediction['size'], ['XS', 'S', 'M', 'L', 'XL', 'XXL'])

        # Test with insufficient measurements
        insufficient_measurements = {'height': 170.0}
        prediction = self.predictor._predict_top_size(insufficient_measurements)
        self.assertIsNone(prediction)

    def test_predict_bottom_size(self):
        """Test bottom size prediction."""
        prediction = self.predictor._predict_bottom_size(self.mock_measurements)

        if prediction is not None:
            self.assertIsInstance(prediction, dict)
            self.assertIn('size', prediction)
            self.assertIn('confidence', prediction)
            self.assertIn('fit_notes', prediction)

            # Check size validity
            self.assertIn(prediction['size'], ['XS', 'S', 'M', 'L', 'XL', 'XXL'])

    def test_predict_dress_size(self):
        """Test dress size prediction."""
        prediction = self.predictor._predict_dress_size(self.mock_measurements)

        if prediction is not None:
            self.assertIsInstance(prediction, dict)
            self.assertIn('size', prediction)
            self.assertIn('confidence', prediction)
            self.assertIn('fit_notes', prediction)

    def test_predict_outerwear_size(self):
        """Test outerwear size prediction."""
        prediction = self.predictor._predict_outerwear_size(self.mock_measurements)

        if prediction is not None:
            self.assertIsInstance(prediction, dict)
            self.assertIn('size', prediction)
            self.assertIn('confidence', prediction)
            self.assertIn('fit_notes', prediction)

    def test_find_best_size_match(self):
        """Test best size matching logic."""
        # Mock size chart
        size_chart = {
            'S': {'chest': 90, 'waist': 75},
            'M': {'chest': 95, 'waist': 80},
            'L': {'chest': 100, 'waist': 85}
        }

        measurements = {'chest': 95, 'waist': 80}

        best_match = self.predictor._find_best_size_match(
            measurements, size_chart, 'chest'
        )

        if best_match is not None:
            self.assertIsInstance(best_match, dict)
            self.assertIn('size', best_match)
            self.assertIn('confidence', best_match)
            self.assertEqual(best_match['size'], 'M')  # Should match M perfectly

    def test_calculate_fit_score(self):
        """Test fit score calculation."""
        user_measurements = {'chest': 95, 'waist': 80}
        size_measurements = {'chest': 95, 'waist': 80}

        # Perfect match should give score close to 0
        score = self.predictor._calculate_fit_score(user_measurements, size_measurements)
        self.assertAlmostEqual(score, 0.0, places=2)

        # Different measurements should give higher score
        size_measurements = {'chest': 100, 'waist': 85}
        score = self.predictor._calculate_fit_score(user_measurements, size_measurements)
        self.assertGreater(score, 0.0)

    def test_calculate_confidence(self):
        """Test confidence calculation from fit score."""
        # Low fit score should give high confidence
        confidence = self.predictor._calculate_confidence(0.05)
        self.assertGreaterEqual(confidence, 0.9)

        # High fit score should give lower confidence
        confidence = self.predictor._calculate_confidence(0.5)
        self.assertLessEqual(confidence, 0.7)

        # All confidence values should be between 0 and 1
        for fit_score in [0.0, 0.1, 0.2, 0.3, 0.5, 1.0]:
            confidence = self.predictor._calculate_confidence(fit_score)
            self.assertGreaterEqual(confidence, 0.0)
            self.assertLessEqual(confidence, 1.0)

    def test_generate_fit_notes(self):
        """Test fit notes generation."""
        size_match = {
            'size': 'M',
            'confidence': 0.85,
            'size_measurements': {'chest': 95, 'waist': 80}
        }

        fit_notes = self.predictor._generate_fit_notes(
            self.mock_measurements, size_match, 'top'
        )

        self.assertIsInstance(fit_notes, list)
        self.assertGreater(len(fit_notes), 0)  # Should have at least one note

        for note in fit_notes:
            self.assertIsInstance(note, str)
            self.assertGreater(len(note), 0)  # Each note should be non-empty

if __name__ == '__main__':
    unittest.main()
