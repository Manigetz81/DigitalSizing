#!/usr/bin/env python3
"""
Test script to validate the Digital Sizing application deployment
"""

import requests
import json
import sys
import os
from pathlib import Path

def test_application(base_url):
    """Test the deployed application endpoints"""
    
    print(f"Testing Digital Sizing Application at: {base_url}")
    print("=" * 50)
    
    # Test 1: Home page
    print("Test 1: Home page accessibility...")
    try:
        response = requests.get(f"{base_url}/", timeout=30)
        if response.status_code == 200:
            print("✅ Home page accessible")
        else:
            print(f"❌ Home page failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Home page error: {e}")
        return False
    
    # Test 2: Health check (if available)
    print("\nTest 2: Application health...")
    try:
        # Try to access a simple endpoint
        response = requests.get(f"{base_url}/", timeout=30)
        if "Digital Sizing" in response.text:
            print("✅ Application is running correctly")
        else:
            print("❌ Application content not found")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 3: API endpoint structure
    print("\nTest 3: API endpoint...")
    try:
        # Test API endpoint without file (should return error)
        response = requests.post(f"{base_url}/api/analyze", timeout=30)
        if response.status_code == 400:  # Expected error for missing file
            print("✅ API endpoint responding correctly")
        else:
            print(f"⚠️  API endpoint returned: {response.status_code}")
    except Exception as e:
        print(f"❌ API endpoint error: {e}")
        return False
    
    print("\n✅ All basic tests passed!")
    return True

def test_with_image(base_url, image_path):
    """Test image upload functionality"""
    
    if not os.path.exists(image_path):
        print(f"❌ Test image not found: {image_path}")
        return False
    
    print(f"\nTesting image upload with: {image_path}")
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{base_url}/api/analyze", files=files, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Image processing successful")
            print(f"   Measurements: {len(result.get('measurements', {}))} items")
            print(f"   Confidence: {result.get('confidence', 'N/A')}")
            return True
        else:
            print(f"❌ Image processing failed: {response.status_code}")
            if response.headers.get('content-type', '').startswith('application/json'):
                print(f"   Error: {response.json().get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Image upload error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_deployment.py <app-url> [test-image-path]")
        print("Example: python test_deployment.py https://your-app.azurewebsites.net")
        sys.exit(1)
    
    app_url = sys.argv[1].rstrip('/')
    
    # Run basic tests
    success = test_application(app_url)
    
    # Test with image if provided
    if len(sys.argv) > 2:
        image_path = sys.argv[2]
        success = success and test_with_image(app_url, image_path)
    
    if success:
        print("\n🎉 Deployment test completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Check the application logs.")
        sys.exit(1)
