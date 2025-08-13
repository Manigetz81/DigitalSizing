"""
Size Prediction and Recommendation System
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
import logging

from utils.size_charts import SizeCharts

logger = logging.getLogger(__name__)

class SizePredictor:
    """
    Predicts clothing sizes based on body measurements.
    """

    def __init__(self):
        """Initialize size predictor with size charts."""
        self.size_charts = SizeCharts()
        self.confidence_threshold = 0.7

    def predict_sizes(self, measurements: Dict[str, float]) -> Dict[str, Dict[str, any]]:
        """
        Predict clothing sizes for different garment types.

        Args:
            measurements: Dictionary of body measurements in centimeters

        Returns:
            Dictionary with size predictions for different clothing types
        """
        try:
            predictions = {}

            # Predict sizes for different clothing categories
            predictions['tops'] = self._predict_top_size(measurements)
            predictions['bottoms'] = self._predict_bottom_size(measurements)
            predictions['dresses'] = self._predict_dress_size(measurements)
            predictions['outerwear'] = self._predict_outerwear_size(measurements)

            # Filter out failed predictions
            predictions = {k: v for k, v in predictions.items() if v is not None}

            logger.info(f"Generated size predictions for {len(predictions)} categories")
            return predictions

        except Exception as e:
            logger.error(f"Error predicting sizes: {str(e)}")
            return {}

    def _predict_top_size(self, measurements: Dict[str, float]) -> Optional[Dict[str, any]]:
        """Predict size for tops/shirts."""
        try:
            required_measurements = ['chest_circumference', 'shoulder_width']

            if not all(m in measurements for m in required_measurements):
                logger.warning("Missing measurements for top size prediction")
                return None

            chest = measurements['chest_circumference']
            shoulder = measurements['shoulder_width']

            # Get size chart for tops
            size_chart = self.size_charts.get_tops_chart()

            # Find best matching size
            best_match = self._find_best_size_match(
                measurements={'chest': chest, 'shoulder': shoulder},
                size_chart=size_chart,
                primary_measurement='chest'
            )

            if best_match:
                return {
                    'size': best_match['size'],
                    'confidence': best_match['confidence'],
                    'fit_notes': self._generate_fit_notes(measurements, best_match, 'top')
                }

            return None

        except Exception as e:
            logger.error(f"Error predicting top size: {str(e)}")
            return None

    def _predict_bottom_size(self, measurements: Dict[str, float]) -> Optional[Dict[str, any]]:
        """Predict size for pants/bottoms."""
        try:
            required_measurements = ['waist_circumference', 'hip_circumference']

            if not all(m in measurements for m in required_measurements):
                logger.warning("Missing measurements for bottom size prediction")
                return None

            waist = measurements['waist_circumference']
            hip = measurements['hip_circumference']

            # Get size chart for bottoms
            size_chart = self.size_charts.get_bottoms_chart()

            # Find best matching size
            best_match = self._find_best_size_match(
                measurements={'waist': waist, 'hip': hip},
                size_chart=size_chart,
                primary_measurement='waist'
            )

            if best_match:
                return {
                    'size': best_match['size'],
                    'confidence': best_match['confidence'],
                    'fit_notes': self._generate_fit_notes(measurements, best_match, 'bottom')
                }

            return None

        except Exception as e:
            logger.error(f"Error predicting bottom size: {str(e)}")
            return None

    def _predict_dress_size(self, measurements: Dict[str, float]) -> Optional[Dict[str, any]]:
        """Predict size for dresses."""
        try:
            required_measurements = ['chest_circumference', 'waist_circumference', 'hip_circumference']

            if not all(m in measurements for m in required_measurements):
                logger.warning("Missing measurements for dress size prediction")
                return None

            chest = measurements['chest_circumference']
            waist = measurements['waist_circumference']
            hip = measurements['hip_circumference']

            # Get size chart for dresses
            size_chart = self.size_charts.get_dresses_chart()

            # Find best matching size using multiple measurements
            best_match = self._find_best_size_match(
                measurements={'chest': chest, 'waist': waist, 'hip': hip},
                size_chart=size_chart,
                primary_measurement='chest'
            )

            if best_match:
                return {
                    'size': best_match['size'],
                    'confidence': best_match['confidence'],
                    'fit_notes': self._generate_fit_notes(measurements, best_match, 'dress')
                }

            return None

        except Exception as e:
            logger.error(f"Error predicting dress size: {str(e)}")
            return None

    def _predict_outerwear_size(self, measurements: Dict[str, float]) -> Optional[Dict[str, any]]:
        """Predict size for jackets/outerwear."""
        try:
            required_measurements = ['chest_circumference', 'shoulder_width']

            if not all(m in measurements for m in required_measurements):
                logger.warning("Missing measurements for outerwear size prediction")
                return None

            chest = measurements['chest_circumference']
            shoulder = measurements['shoulder_width']
            arm_length = measurements.get('arm_length', 0)

            # Get size chart for outerwear (similar to tops but with allowance for layering)
            size_chart = self.size_charts.get_outerwear_chart()

            # Find best matching size
            measurements_dict = {'chest': chest, 'shoulder': shoulder}
            if arm_length > 0:
                measurements_dict['arm_length'] = arm_length

            best_match = self._find_best_size_match(
                measurements=measurements_dict,
                size_chart=size_chart,
                primary_measurement='chest'
            )

            if best_match:
                return {
                    'size': best_match['size'],
                    'confidence': best_match['confidence'],
                    'fit_notes': self._generate_fit_notes(measurements, best_match, 'outerwear')
                }

            return None

        except Exception as e:
            logger.error(f"Error predicting outerwear size: {str(e)}")
            return None

    def _find_best_size_match(self, measurements: Dict[str, float],
                             size_chart: Dict[str, Dict[str, float]],
                             primary_measurement: str) -> Optional[Dict[str, any]]:
        """
        Find the best size match from a size chart.

        Args:
            measurements: User's measurements
            size_chart: Size chart data
            primary_measurement: Primary measurement to use for matching

        Returns:
            Best size match with confidence score
        """
        try:
            if not size_chart or primary_measurement not in measurements:
                return None

            best_size = None
            best_score = float('inf')

            for size, size_measurements in size_chart.items():
                # Calculate fit score for this size
                score = self._calculate_fit_score(measurements, size_measurements)

                if score < best_score:
                    best_score = score
                    best_size = size

            if best_size is None:
                return None

            # Calculate confidence based on fit score
            confidence = self._calculate_confidence(best_score)

            return {
                'size': best_size,
                'confidence': confidence,
                'fit_score': best_score,
                'size_measurements': size_chart[best_size]
            }

        except Exception as e:
            logger.error(f"Error finding best size match: {str(e)}")
            return None

    def _calculate_fit_score(self, user_measurements: Dict[str, float],
                           size_measurements: Dict[str, float]) -> float:
        """
        Calculate how well user measurements fit a size.
        Lower score = better fit.
        """
        try:
            total_score = 0.0
            measurement_count = 0

            # Weights for different measurements
            measurement_weights = {
                'chest': 1.0,
                'waist': 1.0,
                'hip': 1.0,
                'shoulder': 0.8,
                'arm_length': 0.6
            }

            for measurement, user_value in user_measurements.items():
                if measurement in size_measurements:
                    size_value = size_measurements[measurement]
                    weight = measurement_weights.get(measurement, 1.0)

                    # Calculate relative difference
                    diff = abs(user_value - size_value) / size_value
                    weighted_diff = diff * weight

                    total_score += weighted_diff
                    measurement_count += weight

            if measurement_count == 0:
                return float('inf')

            return total_score / measurement_count

        except Exception as e:
            logger.error(f"Error calculating fit score: {str(e)}")
            return float('inf')

    def _calculate_confidence(self, fit_score: float) -> float:
        """Convert fit score to confidence percentage."""
        try:
            # Lower fit score = higher confidence
            # Fit score of 0.1 (10% difference) = 90% confidence
            # Fit score of 0.2 (20% difference) = 80% confidence

            if fit_score <= 0.05:  # 5% difference or less
                return 0.95
            elif fit_score <= 0.1:  # 10% difference or less
                return 0.9
            elif fit_score <= 0.15:  # 15% difference or less
                return 0.85
            elif fit_score <= 0.2:  # 20% difference or less
                return 0.8
            elif fit_score <= 0.3:  # 30% difference or less
                return 0.7
            else:
                return max(0.5, 1.0 - fit_score)  # Minimum 50% confidence

        except Exception as e:
            logger.error(f"Error calculating confidence: {str(e)}")
            return 0.5

    def _generate_fit_notes(self, measurements: Dict[str, float],
                           size_match: Dict[str, any],
                           garment_type: str) -> List[str]:
        """Generate fit notes and recommendations."""
        try:
            notes = []
            user_measurements = measurements
            size_measurements = size_match['size_measurements']

            # Compare measurements and generate notes
            for measurement, user_value in user_measurements.items():
                if measurement in size_measurements:
                    size_value = size_measurements[measurement]
                    diff_percentage = (user_value - size_value) / size_value * 100

                    if abs(diff_percentage) > 15:  # Significant difference
                        if diff_percentage > 0:
                            notes.append(f"Your {measurement} is {abs(diff_percentage):.1f}% larger than average for this size")
                        else:
                            notes.append(f"Your {measurement} is {abs(diff_percentage):.1f}% smaller than average for this size")

            # Add garment-specific recommendations
            if garment_type == 'top':
                if size_match['confidence'] < 0.8:
                    notes.append("Consider trying adjacent sizes for the best fit")
            elif garment_type == 'bottom':
                if 'waist_circumference' in measurements and 'hip_circumference' in measurements:
                    waist = measurements['waist_circumference']
                    hip = measurements['hip_circumference']
                    if hip - waist > 25:
                        notes.append("Consider a pear-shaped fit for better hip accommodation")

            if size_match['confidence'] > 0.9:
                notes.append("Excellent size match - this should fit very well")
            elif size_match['confidence'] > 0.8:
                notes.append("Good size match - should fit well")
            elif size_match['confidence'] > 0.7:
                notes.append("Reasonable fit - consider trying on if possible")
            else:
                notes.append("Uncertain fit - recommend trying on or checking return policy")

            return notes

        except Exception as e:
            logger.error(f"Error generating fit notes: {str(e)}")
            return ["Unable to generate fit recommendations"]
