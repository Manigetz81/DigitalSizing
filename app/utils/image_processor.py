"""
Image Processing Utilities
"""

import cv2
import numpy as np
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class ImageProcessor:
    """
    Handles image preprocessing and optimization for body detection.
    """

    def __init__(self):
        """Initialize image processor with default settings."""
        self.target_width = 640
        self.target_height = 480
        self.min_resolution = (100, 100)  # Reduced minimum size to handle smaller images
        self.max_resolution = (1920, 1080)

    def preprocess(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for optimal body detection.

        Args:
            image: Input image as numpy array

        Returns:
            Preprocessed image
        """
        try:
            if image is None:
                raise ValueError("Input image is None")

            # Validate image
            if not self._validate_image(image):
                raise ValueError("Invalid image format or size")

            # Resize image if needed
            processed_image = self._resize_image(image)

            # Enhance image quality
            processed_image = self._enhance_image(processed_image)

            # Normalize lighting
            processed_image = self._normalize_lighting(processed_image)

            logger.info(f"Preprocessed image to shape: {processed_image.shape}")
            return processed_image

        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            raise

    def _validate_image(self, image: np.ndarray) -> bool:
        """Validate image format and basic properties."""
        try:
            # Check if image is valid numpy array
            if not isinstance(image, np.ndarray):
                return False

            # Check image dimensions
            if len(image.shape) not in [2, 3]:
                return False

            # Check image size
            height, width = image.shape[:2]
            if height < self.min_resolution[1] or width < self.min_resolution[0]:
                logger.warning(f"Image too small: {width}x{height}")
                return False

            if height > self.max_resolution[1] or width > self.max_resolution[0]:
                logger.warning(f"Image very large: {width}x{height}")

            # Check image data type
            if image.dtype not in [np.uint8, np.float32, np.float64]:
                return False

            return True

        except Exception as e:
            logger.error(f"Error validating image: {str(e)}")
            return False

    def _resize_image(self, image: np.ndarray) -> np.ndarray:
        """
        Resize image while maintaining aspect ratio.

        Args:
            image: Input image

        Returns:
            Resized image
        """
        try:
            height, width = image.shape[:2]

            # Calculate aspect ratio
            aspect_ratio = width / height

            # Determine new dimensions
            if aspect_ratio > 1:  # Landscape
                new_width = self.target_width
                new_height = int(self.target_width / aspect_ratio)
            else:  # Portrait or square
                new_height = self.target_height
                new_width = int(self.target_height * aspect_ratio)

            # Ensure minimum size
            new_width = max(new_width, self.min_resolution[0])
            new_height = max(new_height, self.min_resolution[1])

            # Resize image
            resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

            logger.debug(f"Resized image from {width}x{height} to {new_width}x{new_height}")
            return resized_image

        except Exception as e:
            logger.error(f"Error resizing image: {str(e)}")
            return image

    def _enhance_image(self, image: np.ndarray) -> np.ndarray:
        """
        Enhance image quality for better body detection.

        Args:
            image: Input image

        Returns:
            Enhanced image
        """
        try:
            # Convert to LAB color space for better processing
            if len(image.shape) == 3:
                lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

                # Split channels
                l_channel, a_channel, b_channel = cv2.split(lab_image)

                # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to L channel
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                l_channel = clahe.apply(l_channel)

                # Merge channels back
                enhanced_lab = cv2.merge([l_channel, a_channel, b_channel])

                # Convert back to BGR
                enhanced_image = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
            else:
                # Grayscale image
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                enhanced_image = clahe.apply(image)

            return enhanced_image

        except Exception as e:
            logger.error(f"Error enhancing image: {str(e)}")
            return image

    def _normalize_lighting(self, image: np.ndarray) -> np.ndarray:
        """
        Normalize lighting conditions in the image.

        Args:
            image: Input image

        Returns:
            Image with normalized lighting
        """
        try:
            if len(image.shape) == 3:
                # Convert to float for processing
                normalized = image.astype(np.float32) / 255.0

                # Calculate per-channel mean
                mean_values = np.mean(normalized, axis=(0, 1))

                # Adjust brightness if too dark or too bright
                target_brightness = 0.5
                for i in range(3):
                    if mean_values[i] < 0.3:  # Too dark
                        normalized[:, :, i] = np.clip(normalized[:, :, i] * 1.2, 0, 1)
                    elif mean_values[i] > 0.7:  # Too bright
                        normalized[:, :, i] = np.clip(normalized[:, :, i] * 0.8, 0, 1)

                # Convert back to uint8
                normalized_image = (normalized * 255).astype(np.uint8)
            else:
                # Grayscale normalization
                normalized_image = cv2.equalizeHist(image)

            return normalized_image

        except Exception as e:
            logger.error(f"Error normalizing lighting: {str(e)}")
            return image

    def crop_to_person(self, image: np.ndarray, landmarks: dict) -> np.ndarray:
        """
        Crop image to focus on the detected person.

        Args:
            image: Input image
            landmarks: Detected body landmarks

        Returns:
            Cropped image
        """
        try:
            if not landmarks:
                return image

            # Find bounding box of all landmarks
            x_coords = [coord[0] for coord in landmarks.values()]
            y_coords = [coord[1] for coord in landmarks.values()]

            min_x = max(0, int(min(x_coords)) - 50)
            max_x = min(image.shape[1], int(max(x_coords)) + 50)
            min_y = max(0, int(min(y_coords)) - 50)
            max_y = min(image.shape[0], int(max(y_coords)) + 50)

            # Crop image
            cropped_image = image[min_y:max_y, min_x:max_x]

            logger.debug(f"Cropped image to region: ({min_x}, {min_y}) to ({max_x}, {max_y})")
            return cropped_image

        except Exception as e:
            logger.error(f"Error cropping image: {str(e)}")
            return image

    def add_padding(self, image: np.ndarray, padding: int = 20) -> np.ndarray:
        """
        Add padding around the image.

        Args:
            image: Input image
            padding: Padding size in pixels

        Returns:
            Padded image
        """
        try:
            if len(image.shape) == 3:
                padded_image = cv2.copyMakeBorder(
                    image, padding, padding, padding, padding,
                    cv2.BORDER_REFLECT_101
                )
            else:
                padded_image = cv2.copyMakeBorder(
                    image, padding, padding, padding, padding,
                    cv2.BORDER_REFLECT_101
                )

            return padded_image

        except Exception as e:
            logger.error(f"Error adding padding: {str(e)}")
            return image

    def convert_color_space(self, image: np.ndarray, conversion: str) -> np.ndarray:
        """
        Convert image between color spaces.

        Args:
            image: Input image
            conversion: Color space conversion (e.g., 'BGR2RGB', 'BGR2GRAY')

        Returns:
            Converted image
        """
        try:
            conversion_map = {
                'BGR2RGB': cv2.COLOR_BGR2RGB,
                'RGB2BGR': cv2.COLOR_RGB2BGR,
                'BGR2GRAY': cv2.COLOR_BGR2GRAY,
                'GRAY2BGR': cv2.COLOR_GRAY2BGR,
                'BGR2HSV': cv2.COLOR_BGR2HSV,
                'HSV2BGR': cv2.COLOR_HSV2BGR
            }

            if conversion in conversion_map:
                converted_image = cv2.cvtColor(image, conversion_map[conversion])
                return converted_image
            else:
                logger.warning(f"Unknown color conversion: {conversion}")
                return image

        except Exception as e:
            logger.error(f"Error converting color space: {str(e)}")
            return image
