<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Digital Sizing Project - Copilot Instructions

This is a Python computer vision project for determining apparel sizes based on person images.

## Project Context
- **Main Purpose**: Analyze images of people to recommend clothing sizes
- **Technology Stack**: Python, Flask, OpenCV, MediaPipe, TensorFlow, scikit-learn
- **Architecture**: Web application with REST API endpoints

## Key Components
1. **Body Detection**: Use MediaPipe for pose estimation and body keypoint detection
2. **Measurement Calculation**: Convert pixel coordinates to real-world measurements
3. **Size Recommendation**: Map measurements to standard clothing size charts
4. **Web Interface**: Flask-based UI for image upload and results display

## Coding Guidelines
- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Add comprehensive docstrings for all classes and functions
- Implement proper error handling for image processing operations
- Use numpy arrays for efficient numerical computations
- Validate image inputs (format, size, content)

## File Structure Notes
- `app/models/`: Core ML models and algorithms
- `app/utils/`: Utility functions for image processing and size charts
- `app/static/`: Frontend assets and uploaded images
- `tests/`: Unit tests for all components
- `data/`: Sample data and size chart references

## MediaPipe Integration
- Use MediaPipe Pose for body landmark detection
- Extract key measurements: height, chest, waist, hip, shoulder width
- Handle cases where full body is not visible in image
- Implement confidence scoring for landmark detection

## Size Calculation Logic
- Convert pixel distances to real-world measurements using reference objects or body proportions
- Apply gender-specific measurement adjustments
- Support multiple clothing categories (tops, bottoms, dresses, outerwear)
- Provide size recommendations with confidence levels

## Error Handling
- Gracefully handle images without detectable people
- Validate image quality and resolution requirements
- Provide meaningful error messages for users
- Log errors for debugging purposes

## Performance Considerations
- Optimize image processing for web deployment
- Implement caching for repeated calculations
- Use efficient data structures for size chart lookups
- Consider memory usage when processing large images
