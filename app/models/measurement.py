"""
Body Measurement Calculation from Landmarks
"""

import numpy as np
import math
from typing import Dict, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class MeasurementCalculator:
    """
    Calculates body measurements from detected landmarks.
    """

    def __init__(self):
        """Initialize measurement calculator with reference ratios."""
        # Average human body proportions (head height as reference)
        self.body_proportions = {
            'head_to_total_height': 1/8,
            'shoulder_to_height': 1/4,
            'torso_to_height': 3/8,
            'arm_to_height': 3/8,
            'leg_to_height': 1/2
        }

        # Conversion factors for different measurement types
        self.measurement_factors = {
            'chest_width_to_circumference': 2.8,  # More realistic ratio (not full π)
            'waist_width_to_circumference': 2.6,  # Waist is more elliptical
            'hip_width_to_circumference': 2.8     # Similar to chest
        }

    def calculate_measurements(self, landmarks: Dict[str, Tuple[float, float]],
                             image_shape: Tuple[int, int]) -> Dict[str, float]:
        """
        Calculate body measurements from landmarks.

        Args:
            landmarks: Dictionary of landmark coordinates
            image_shape: Shape of the image (height, width)

        Returns:
            Dictionary of measurements in centimeters
        """
        try:
            measurements = {}

            # Calculate reference scale (pixels per cm)
            scale_factor = self._calculate_scale_factor(landmarks, image_shape)

            # Add detailed logging for debugging
            logger.info(f"Image shape: {image_shape}")
            logger.info(f"Calculated scale factor: {scale_factor}")

            if scale_factor is None:
                logger.error("Could not determine scale factor")
                return {}

            # Calculate individual measurements
            measurements['height'] = self._calculate_height(landmarks, scale_factor)
            measurements['shoulder_width'] = self._calculate_shoulder_width(landmarks, scale_factor)
            measurements['chest_circumference'] = self._calculate_chest_circumference(landmarks, scale_factor)
            measurements['waist_circumference'] = self._calculate_waist_circumference(landmarks, scale_factor)
            measurements['hip_circumference'] = self._calculate_hip_circumference(landmarks, scale_factor)
            measurements['arm_length'] = self._calculate_arm_length(landmarks, scale_factor)

            # Add debug logging for measurements
            for measurement, value in measurements.items():
                if value is not None:
                    logger.info(f"Calculated {measurement}: {value}")
                else:
                    logger.warning(f"Could not calculate {measurement}")

            # Filter out None values
            measurements = {k: v for k, v in measurements.items() if v is not None}

            logger.info(f"Calculated {len(measurements)} measurements")
            return measurements

        except Exception as e:
            logger.error(f"Error calculating measurements: {str(e)}")
            return {}

    def _calculate_scale_factor(self, landmarks: Dict[str, Tuple[float, float]],
                               image_shape: Tuple[int, int]) -> Optional[float]:
        """
        Calculate pixels per centimeter using body proportions as reference.
        Uses multiple methods and averages them for better accuracy.

        Args:
            landmarks: Landmark coordinates
            image_shape: Image dimensions

        Returns:
            Scale factor (pixels per cm) or None if calculation fails
        """
        try:
            scale_factors = []

            # Method 1: Use shoulder width as reference
            if 'LEFT_SHOULDER' in landmarks and 'RIGHT_SHOULDER' in landmarks:
                shoulder_width_pixels = self._calculate_distance(
                    landmarks['LEFT_SHOULDER'], landmarks['RIGHT_SHOULDER']
                )
                # Average adult shoulder width varies: use conservative estimate
                average_shoulder_width_cm = 40.0  # Slightly smaller for better overall scaling
                scale_factor = shoulder_width_pixels / average_shoulder_width_cm

                # Validate scale factor (reasonable range for different photo distances)
                if 0.5 <= scale_factor <= 15.0:
                    scale_factors.append(('shoulders', scale_factor))
                    logger.info(f"Scale factor from shoulders: {scale_factor:.2f} px/cm (shoulder width: {shoulder_width_pixels:.1f} px)")

            # Method 2: Use hip width as reference (alternative body measurement)
            if 'LEFT_HIP' in landmarks and 'RIGHT_HIP' in landmarks:
                hip_width_pixels = self._calculate_distance(
                    landmarks['LEFT_HIP'], landmarks['RIGHT_HIP']
                )
                # Average adult hip width is roughly 35-40cm
                average_hip_width_cm = 36.0
                scale_factor = hip_width_pixels / average_hip_width_cm

                if 0.5 <= scale_factor <= 15.0:
                    scale_factors.append(('hips', scale_factor))
                    logger.info(f"Scale factor from hips: {scale_factor:.2f} px/cm (hip width: {hip_width_pixels:.1f} px)")

            # Method 3: Use image dimensions to estimate scale (fallback)
            if image_shape:
                image_height = image_shape[0]
                estimated_person_height_pixels = image_height * 0.85
                average_height_cm = 165.0  # Conservative estimate
                scale_factor = estimated_person_height_pixels / average_height_cm

                if 0.3 <= scale_factor <= 20.0:
                    scale_factors.append(('image_height', scale_factor))
                    logger.info(f"Scale factor from image height: {scale_factor:.2f} px/cm")

            # Choose the best scale factor
            if scale_factors:
                # Prefer shoulder measurement, then hip, then image height
                if any(method == 'shoulders' for method, _ in scale_factors):
                    chosen_scale = next(sf for method, sf in scale_factors if method == 'shoulders')
                    logger.info(f"Using shoulder-based scale factor: {chosen_scale:.2f} px/cm")
                elif any(method == 'hips' for method, _ in scale_factors):
                    chosen_scale = next(sf for method, sf in scale_factors if method == 'hips')
                    logger.info(f"Using hip-based scale factor: {chosen_scale:.2f} px/cm")
                else:
                    chosen_scale = scale_factors[0][1]
                    logger.info(f"Using fallback scale factor: {chosen_scale:.2f} px/cm")

                return chosen_scale

            logger.warning("Could not calculate reliable scale factor")
            return None

        except Exception as e:
            logger.error(f"Error calculating scale factor: {str(e)}")
            return None

    def _calculate_distance(self, point1: Tuple[float, float],
                           point2: Tuple[float, float]) -> float:
        """Calculate Euclidean distance between two points."""
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

    def _calculate_height(self, landmarks: Dict[str, Tuple[float, float]],
                         scale_factor: float) -> Optional[float]:
        """Calculate total body height."""
        try:
            if 'NOSE' not in landmarks:
                logger.warning("Height calculation failed: NOSE landmark missing")
                return None

            nose = landmarks['NOSE']

            # Use average of both ankles if available, otherwise use available ankle
            ankle_points = []
            if 'LEFT_ANKLE' in landmarks:
                ankle_points.append(landmarks['LEFT_ANKLE'])
            if 'RIGHT_ANKLE' in landmarks:
                ankle_points.append(landmarks['RIGHT_ANKLE'])

            if not ankle_points:
                logger.warning("Height calculation failed: No ankle landmarks found")
                return None

            # Average ankle position (or single ankle if only one available)
            avg_ankle = (
                sum(float(p[0]) for p in ankle_points) / len(ankle_points),
                sum(float(p[1]) for p in ankle_points) / len(ankle_points)
            )

            # Calculate distance from nose to ankles
            nose_to_ankle_pixels = self._calculate_distance(
                (float(nose[0]), float(nose[1])), avg_ankle
            )

            # Estimate head top from nose position
            # Add head height: nose to top of head is roughly 6% of total body length
            head_top_offset = nose_to_ankle_pixels * 0.06
            total_height_pixels = nose_to_ankle_pixels + head_top_offset

            height_cm = total_height_pixels / scale_factor

            logger.info(f"Height calculation: nose_to_ankle={nose_to_ankle_pixels:.1f}px, "
                       f"head_offset={head_top_offset:.1f}px, total={total_height_pixels:.1f}px, "
                       f"height={height_cm:.1f}cm")

            # Validate height (reasonable human height range - expanded for edge cases)
            if 120 < height_cm < 250:
                return round(height_cm, 1)
            else:
                logger.warning(f"Height {height_cm:.1f}cm outside valid range (120-250cm)")

            return None

        except Exception as e:
            logger.error(f"Error calculating height: {str(e)}")
            return None

    def _calculate_shoulder_width(self, landmarks: Dict[str, Tuple[float, float]],
                                 scale_factor: float) -> Optional[float]:
        """Calculate shoulder width."""
        try:
            if 'LEFT_SHOULDER' not in landmarks or 'RIGHT_SHOULDER' not in landmarks:
                return None

            left_shoulder = landmarks['LEFT_SHOULDER']
            right_shoulder = landmarks['RIGHT_SHOULDER']

            width_pixels = self._calculate_distance(left_shoulder, right_shoulder)
            width_cm = width_pixels / scale_factor

            # Validate shoulder width
            if 20 < width_cm < 80:
                return round(width_cm, 1)

            return None

        except Exception as e:
            logger.error(f"Error calculating shoulder width: {str(e)}")
            return None

    def _calculate_chest_circumference(self, landmarks: Dict[str, Tuple[float, float]],
                                     scale_factor: float) -> Optional[float]:
        """Calculate chest circumference from shoulder and torso landmarks."""
        try:
            if 'LEFT_SHOULDER' not in landmarks or 'RIGHT_SHOULDER' not in landmarks:
                return None

            # Use shoulder width as basis for chest measurement
            shoulder_width_pixels = self._calculate_distance(
                landmarks['LEFT_SHOULDER'], landmarks['RIGHT_SHOULDER']
            )
            shoulder_width_cm = shoulder_width_pixels / scale_factor

            # Estimate chest width as approximately 85% of shoulder width
            # (chest is measured under the arms, shoulders extend beyond this)
            chest_width = shoulder_width_cm * 0.85

            # Convert width to circumference approximation
            chest_circumference = chest_width * self.measurement_factors['chest_width_to_circumference']

            # Validate chest circumference
            if 70 < chest_circumference < 150:
                return round(chest_circumference, 1)

            return None

        except Exception as e:
            logger.error(f"Error calculating chest circumference: {str(e)}")
            return None

    def _calculate_waist_circumference(self, landmarks: Dict[str, Tuple[float, float]],
                                     scale_factor: float) -> Optional[float]:
        """Calculate waist circumference."""
        try:
            if 'LEFT_HIP' not in landmarks or 'RIGHT_HIP' not in landmarks:
                return None

            # Use hip landmarks as waist approximation
            left_hip = landmarks['LEFT_HIP']
            right_hip = landmarks['RIGHT_HIP']

            hip_width_pixels = self._calculate_distance(left_hip, right_hip)
            hip_width_cm = hip_width_pixels / scale_factor

            # Waist is typically 70-80% of hip width
            waist_width = hip_width_cm * 0.75

            # Convert to circumference
            waist_circumference = waist_width * self.measurement_factors['waist_width_to_circumference']

            # Validate waist circumference
            if 60 < waist_circumference < 120:
                return round(waist_circumference, 1)

            return None

        except Exception as e:
            logger.error(f"Error calculating waist circumference: {str(e)}")
            return None

    def _calculate_hip_circumference(self, landmarks: Dict[str, Tuple[float, float]],
                                   scale_factor: float) -> Optional[float]:
        """Calculate hip circumference."""
        try:
            if 'LEFT_HIP' not in landmarks or 'RIGHT_HIP' not in landmarks:
                return None

            left_hip = landmarks['LEFT_HIP']
            right_hip = landmarks['RIGHT_HIP']

            hip_width_pixels = self._calculate_distance(left_hip, right_hip)
            hip_width_cm = hip_width_pixels / scale_factor

            # Convert to circumference
            hip_circumference = hip_width_cm * self.measurement_factors['hip_width_to_circumference']

            # Validate hip circumference
            if 75 < hip_circumference < 140:
                return round(hip_circumference, 1)

            return None

        except Exception as e:
            logger.error(f"Error calculating hip circumference: {str(e)}")
            return None

    def _calculate_arm_length(self, landmarks: Dict[str, Tuple[float, float]],
                            scale_factor: float) -> Optional[float]:
        """Calculate arm length from shoulder to wrist."""
        try:
            # Try left arm first, then right arm
            for side in ['LEFT', 'RIGHT']:
                shoulder_key = f'{side}_SHOULDER'
                wrist_key = f'{side}_WRIST'

                if shoulder_key in landmarks and wrist_key in landmarks:
                    shoulder = landmarks[shoulder_key]
                    wrist = landmarks[wrist_key]

                    arm_length_pixels = self._calculate_distance(
                        (float(shoulder[0]), float(shoulder[1])),
                        (float(wrist[0]), float(wrist[1]))
                    )
                    arm_length_cm = arm_length_pixels / scale_factor

                    logger.info(f"Arm length ({side}): {arm_length_pixels:.1f}px = {arm_length_cm:.1f}cm")

                    # Validate arm length (realistic range for human arm length - expanded)
                    if 40 < arm_length_cm < 90:
                        return round(arm_length_cm, 1)
                    else:
                        logger.warning(f"Arm length {arm_length_cm:.1f}cm outside valid range (40-90cm)")

            logger.warning("Could not calculate valid arm length from any arm")
            return None

        except Exception as e:
            logger.error(f"Error calculating arm length: {str(e)}")
            return None
