# Digital Sizing - Apparel Size Determination

An AI-powered application that determines apparel sizes based on person images using computer vision and machine learning.

## Features

- **Image Upload**: Upload photos of people to analyze body measurements
- **Body Detection**: Automatic detection of body keypoints using MediaPipe
- **Size Calculation**: Calculate body measurements from image analysis
- **Size Recommendation**: Recommend apparel sizes based on standard sizing charts
- **Web Interface**: Easy-to-use web interface for image upload and results
- **Multiple Formats**: Support for various image formats (JPG, PNG, etc.)

## Project Structure

```
digital-sizing/
├── app/
│   ├── __init__.py
│   ├── main.py              # Flask web application
│   ├── models/
│   │   ├── __init__.py
│   │   ├── body_detector.py # Body keypoint detection
│   │   ├── measurement.py   # Body measurement calculations
│   │   └── size_predictor.py # Size recommendation logic
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── image_processor.py # Image preprocessing utilities
│   │   └── size_charts.py    # Standard sizing charts
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── uploads/
│   └── templates/
│       ├── index.html
│       └── results.html
├── tests/
│   ├── __init__.py
│   ├── test_body_detector.py
│   ├── test_measurement.py
│   └── test_size_predictor.py
├── data/
│   ├── size_charts/
│   └── sample_images/
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation

1. Clone the repository:
```bash
cd "c:\Mani\Agentic AI\Digital Sizing"
```

2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy environment variables:
```bash
copy .env.example .env
```

## Usage

### Running the Web Application

```bash
python app/main.py
```

The application will be available at `http://localhost:5000`

### API Usage

1. **Upload Image**: POST to `/api/upload`
2. **Get Measurements**: POST to `/api/analyze`
3. **Get Size Recommendation**: POST to `/api/recommend`

## How It Works

1. **Image Upload**: User uploads an image of a person
2. **Body Detection**: MediaPipe detects body keypoints and landmarks
3. **Measurement Extraction**: Calculate body measurements from keypoints
4. **Size Mapping**: Map measurements to standard sizing charts
5. **Recommendation**: Provide size recommendations for different clothing types

## Supported Measurements

- Height
- Chest/Bust circumference
- Waist circumference
- Hip circumference
- Shoulder width
- Arm length

## Supported Clothing Types

- Shirts/Tops
- Pants/Bottoms
- Dresses
- Jackets/Outerwear

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Adding New Size Charts

Add new sizing charts in `app/utils/size_charts.py` following the existing format.

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Disclaimer

This application provides size estimates based on image analysis. Results may vary and should be used as a general guide. For critical fitting requirements, professional measurement is recommended.
