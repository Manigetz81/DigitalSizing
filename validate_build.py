#!/usr/bin/env python3
"""
Build validation script for Digital Sizing application
Validates the application structure and basic imports without full installation
"""

import os
import sys
import importlib.util
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} missing: {filepath}")
        return False

def check_python_syntax(filepath):
    """Check if Python file has valid syntax"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            compile(f.read(), filepath, 'exec')
        print(f"✅ Syntax valid: {filepath}")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error in {filepath}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error checking {filepath}: {e}")
        return False

def validate_project_structure():
    """Validate the project structure"""
    print("Digital Sizing - Build Validation")
    print("=================================")
    
    required_files = [
        ("requirements.txt", "Dependencies file"),
        ("app.py", "WSGI entry point"),
        ("wsgi.py", "Alternative WSGI entry point"),
        ("gunicorn.conf.py", "Gunicorn configuration"),
        ("Procfile", "Process definition"),
        ("runtime.txt", "Python runtime"),
        ("azure-deploy.json", "Azure ARM template"),
        ("app/main.py", "Main Flask application"),
        ("app/__init__.py", "App package init"),
        ("app/models/__init__.py", "Models package init"),
        ("app/utils/__init__.py", "Utils package init"),
        ("app/templates/index.html", "Home template"),
        ("app/templates/results.html", "Results template"),
        ("app/static/css/style.css", "CSS stylesheet"),
    ]
    
    success = True
    
    print("\nChecking required files...")
    for filepath, description in required_files:
        if not check_file_exists(filepath, description):
            success = False
    
    print("\nChecking Python syntax...")
    python_files = [
        "app.py",
        "wsgi.py", 
        "gunicorn.conf.py",
        "app/main.py",
        "app/__init__.py",
        "app/models/__init__.py",
        "app/models/body_detector.py",
        "app/models/measurement.py",
        "app/models/size_predictor.py",
        "app/utils/__init__.py",
        "app/utils/image_processor.py",
        "app/utils/size_charts.py",
    ]
    
    for filepath in python_files:
        if os.path.exists(filepath):
            if not check_python_syntax(filepath):
                success = False
    
    print("\nChecking configuration files...")
    
    # Check requirements.txt
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", 'r') as f:
            requirements = f.read()
            if "Flask" in requirements and "gunicorn" in requirements:
                print("✅ Requirements.txt contains essential packages")
            else:
                print("❌ Requirements.txt missing essential packages")
                success = False
    
    # Check runtime.txt
    if os.path.exists("runtime.txt"):
        with open("runtime.txt", 'r') as f:
            runtime = f.read().strip()
            if runtime.startswith("python-3."):
                print(f"✅ Runtime specified: {runtime}")
            else:
                print(f"❌ Invalid runtime specification: {runtime}")
                success = False
    
    # Check Procfile
    if os.path.exists("Procfile"):
        with open("Procfile", 'r') as f:
            procfile = f.read().strip()
            if "gunicorn" in procfile and "app:application" in procfile:
                print("✅ Procfile correctly configured")
            else:
                print("❌ Procfile configuration issue")
                success = False
    
    print("\nChecking upload directory...")
    upload_dir = "app/static/uploads"
    if os.path.exists(upload_dir):
        print(f"✅ Upload directory exists: {upload_dir}")
        gitkeep_path = os.path.join(upload_dir, ".gitkeep")
        if os.path.exists(gitkeep_path):
            print("✅ .gitkeep file exists in uploads")
        else:
            print("⚠️  .gitkeep file missing in uploads directory")
    else:
        print(f"❌ Upload directory missing: {upload_dir}")
        success = False
    
    return success

def check_azure_requirements():
    """Check Azure-specific requirements"""
    print("\nChecking Azure deployment requirements...")
    
    azure_files = [
        "azure-deploy.json",
        "deploy-to-azure.ps1", 
        "deploy-to-azure.sh",
        "AZURE_DEPLOYMENT_GUIDE.md"
    ]
    
    success = True
    for filepath in azure_files:
        if not check_file_exists(filepath, f"Azure file"):
            success = False
    
    return success

if __name__ == "__main__":
    print("Starting build validation...")
    
    # Change to project directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    structure_valid = validate_project_structure()
    azure_valid = check_azure_requirements()
    
    print("\n" + "="*50)
    
    if structure_valid and azure_valid:
        print("🎉 Build validation PASSED!")
        print("The application is ready for Azure deployment.")
        sys.exit(0)
    else:
        print("❌ Build validation FAILED!")
        print("Please fix the issues above before deploying.")
        sys.exit(1)
