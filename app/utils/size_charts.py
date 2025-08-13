"""
Standard Clothing Size Charts
"""

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class SizeCharts:
    """
    Contains standard clothing size charts for different garment types.
    All measurements are in centimeters.
    """

    def __init__(self):
        """Initialize size charts with standard measurements."""
        self._initialize_charts()

    def _initialize_charts(self) -> None:
        """Initialize all size chart data."""
        # Women's size charts
        self.womens_tops = {
            'XS': {'chest': 81, 'waist': 61, 'shoulder': 35},
            'S': {'chest': 86, 'waist': 66, 'shoulder': 37},
            'M': {'chest': 91, 'waist': 71, 'shoulder': 39},
            'L': {'chest': 97, 'waist': 76, 'shoulder': 41},
            'XL': {'chest': 102, 'waist': 81, 'shoulder': 43},
            'XXL': {'chest': 107, 'waist': 86, 'shoulder': 45}
        }

        self.womens_bottoms = {
            'XS': {'waist': 61, 'hip': 86},
            'S': {'waist': 66, 'hip': 91},
            'M': {'waist': 71, 'hip': 97},
            'L': {'waist': 76, 'hip': 102},
            'XL': {'waist': 81, 'hip': 107},
            'XXL': {'waist': 86, 'hip': 112}
        }

        self.womens_dresses = {
            'XS': {'chest': 81, 'waist': 61, 'hip': 86},
            'S': {'chest': 86, 'waist': 66, 'hip': 91},
            'M': {'chest': 91, 'waist': 71, 'hip': 97},
            'L': {'chest': 97, 'waist': 76, 'hip': 102},
            'XL': {'chest': 102, 'waist': 81, 'hip': 107},
            'XXL': {'chest': 107, 'waist': 86, 'hip': 112}
        }

        # Men's size charts
        self.mens_tops = {
            'XS': {'chest': 86, 'waist': 71, 'shoulder': 42},
            'S': {'chest': 91, 'waist': 76, 'shoulder': 44},
            'M': {'chest': 97, 'waist': 81, 'shoulder': 46},
            'L': {'chest': 102, 'waist': 86, 'shoulder': 48},
            'XL': {'chest': 107, 'waist': 91, 'shoulder': 50},
            'XXL': {'chest': 112, 'waist': 97, 'shoulder': 52}
        }

        self.mens_bottoms = {
            'XS': {'waist': 71, 'hip': 91},
            'S': {'waist': 76, 'hip': 97},
            'M': {'waist': 81, 'hip': 102},
            'L': {'waist': 86, 'hip': 107},
            'XL': {'waist': 91, 'hip': 112},
            'XXL': {'waist': 97, 'hip': 117}
        }

        # Unisex outerwear (with room for layering)
        self.outerwear = {
            'XS': {'chest': 91, 'shoulder': 40, 'arm_length': 59},
            'S': {'chest': 97, 'shoulder': 42, 'arm_length': 61},
            'M': {'chest': 102, 'shoulder': 44, 'arm_length': 63},
            'L': {'chest': 107, 'shoulder': 46, 'arm_length': 65},
            'XL': {'chest': 112, 'shoulder': 48, 'arm_length': 67},
            'XXL': {'chest': 117, 'shoulder': 50, 'arm_length': 69}
        }

        # International size conversions
        self.size_conversions = {
            'US_to_EU': {
                'XS': '32',
                'S': '34',
                'M': '36',
                'L': '38',
                'XL': '40',
                'XXL': '42'
            },
            'US_to_UK': {
                'XS': '6',
                'S': '8',
                'M': '10',
                'L': '12',
                'XL': '14',
                'XXL': '16'
            }
        }

    def get_tops_chart(self, gender: str = 'unisex') -> Dict[str, Dict[str, float]]:
        """
        Get size chart for tops/shirts.

        Args:
            gender: 'men', 'women', or 'unisex'

        Returns:
            Size chart dictionary
        """
        try:
            if gender.lower() == 'men':
                return self.mens_tops.copy()
            elif gender.lower() == 'women':
                return self.womens_tops.copy()
            else:
                # Return average of men's and women's charts for unisex
                unisex_chart = {}
                for size in self.mens_tops.keys():
                    unisex_chart[size] = {}
                    for measurement in self.mens_tops[size].keys():
                        mens_val = self.mens_tops[size][measurement]
                        womens_val = self.womens_tops[size][measurement]
                        unisex_chart[size][measurement] = (mens_val + womens_val) / 2
                return unisex_chart

        except Exception as e:
            logger.error(f"Error getting tops chart: {str(e)}")
            return self.mens_tops.copy()

    def get_bottoms_chart(self, gender: str = 'unisex') -> Dict[str, Dict[str, float]]:
        """
        Get size chart for pants/bottoms.

        Args:
            gender: 'men', 'women', or 'unisex'

        Returns:
            Size chart dictionary
        """
        try:
            if gender.lower() == 'men':
                return self.mens_bottoms.copy()
            elif gender.lower() == 'women':
                return self.womens_bottoms.copy()
            else:
                # Return average for unisex
                unisex_chart = {}
                for size in self.mens_bottoms.keys():
                    unisex_chart[size] = {}
                    for measurement in self.mens_bottoms[size].keys():
                        mens_val = self.mens_bottoms[size][measurement]
                        womens_val = self.womens_bottoms[size][measurement]
                        unisex_chart[size][measurement] = (mens_val + womens_val) / 2
                return unisex_chart

        except Exception as e:
            logger.error(f"Error getting bottoms chart: {str(e)}")
            return self.mens_bottoms.copy()

    def get_dresses_chart(self) -> Dict[str, Dict[str, float]]:
        """Get size chart for dresses."""
        return self.womens_dresses.copy()

    def get_outerwear_chart(self) -> Dict[str, Dict[str, float]]:
        """Get size chart for jackets/outerwear."""
        return self.outerwear.copy()

    def convert_size(self, us_size: str, target_system: str) -> str:
        """
        Convert US size to other sizing systems.

        Args:
            us_size: US size (XS, S, M, L, XL, XXL)
            target_system: Target system ('EU', 'UK')

        Returns:
            Converted size or original if conversion not available
        """
        try:
            conversion_key = f"US_to_{target_system.upper()}"

            if conversion_key in self.size_conversions:
                return self.size_conversions[conversion_key].get(us_size, us_size)

            return us_size

        except Exception as e:
            logger.error(f"Error converting size: {str(e)}")
            return us_size

    def get_size_range_info(self, garment_type: str) -> Dict[str, Dict[str, float]]:
        """
        Get size range information for a garment type.

        Args:
            garment_type: Type of garment ('tops', 'bottoms', 'dresses', 'outerwear')

        Returns:
            Dictionary with min and max measurements for each size
        """
        try:
            if garment_type == 'tops':
                chart = self.get_tops_chart()
            elif garment_type == 'bottoms':
                chart = self.get_bottoms_chart()
            elif garment_type == 'dresses':
                chart = self.get_dresses_chart()
            elif garment_type == 'outerwear':
                chart = self.get_outerwear_chart()
            else:
                return {}

            size_ranges = {}
            sizes = list(chart.keys())

            for i, size in enumerate(sizes):
                size_ranges[size] = {}

                for measurement, value in chart[size].items():
                    # Calculate range based on adjacent sizes
                    min_val = value
                    max_val = value

                    if i > 0:  # Not the smallest size
                        prev_value = chart[sizes[i-1]][measurement]
                        min_val = (prev_value + value) / 2

                    if i < len(sizes) - 1:  # Not the largest size
                        next_value = chart[sizes[i+1]][measurement]
                        max_val = (value + next_value) / 2

                    size_ranges[size][measurement] = {
                        'min': min_val,
                        'max': max_val,
                        'ideal': value
                    }

            return size_ranges

        except Exception as e:
            logger.error(f"Error getting size range info: {str(e)}")
            return {}

    def get_custom_size_chart(self, brand: str, garment_type: str) -> Dict[str, Dict[str, float]]:
        """
        Get brand-specific size chart (placeholder for future brand customization).

        Args:
            brand: Brand name
            garment_type: Type of garment

        Returns:
            Size chart (currently returns standard chart)
        """
        # Placeholder for brand-specific charts
        # In future versions, this could load brand-specific sizing data

        logger.info(f"Using standard chart for {brand} {garment_type} (brand-specific not available)")

        if garment_type == 'tops':
            return self.get_tops_chart()
        elif garment_type == 'bottoms':
            return self.get_bottoms_chart()
        elif garment_type == 'dresses':
            return self.get_dresses_chart()
        elif garment_type == 'outerwear':
            return self.get_outerwear_chart()
        else:
            return self.get_tops_chart()  # Default fallback

    def get_all_charts(self) -> Dict[str, Dict[str, Dict[str, float]]]:
        """Get all available size charts."""
        return {
            'mens_tops': self.mens_tops,
            'womens_tops': self.womens_tops,
            'mens_bottoms': self.mens_bottoms,
            'womens_bottoms': self.womens_bottoms,
            'womens_dresses': self.womens_dresses,
            'outerwear': self.outerwear
        }
