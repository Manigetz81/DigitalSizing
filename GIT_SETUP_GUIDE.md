# Git Repository Setup Guide for Digital Sizing Project

## Prerequisites

1. **Install Git** (if not already installed):
   - Download from: https://git-scm.com/download/windows
   - Install with default settings
   - Restart your terminal/command prompt after installation

2. **Create a GitHub/GitLab/Bitbucket account** (if you don't have one)

## Option 1: Automated Setup (Recommended)

### Using PowerShell (Recommended for Windows):
```powershell
# Navigate to your project directory
cd "c:\Mani\Agentic AI\Digital Sizing"

# Run the PowerShell setup script
.\setup_git.ps1
```

### Using Command Prompt:
```cmd
# Navigate to your project directory
cd "c:\Mani\Agentic AI\Digital Sizing"

# Run the batch setup script
setup_git.bat
```

### Using Python:
```cmd
# Navigate to your project directory
cd "c:\Mani\Agentic AI\Digital Sizing"

# Run the Python setup script
python setup_git_repository.py
```

## Option 2: Manual Setup

### Step 1: Initialize Git Repository
```bash
# Navigate to your project directory
cd "c:\Mani\Agentic AI\Digital Sizing"

# Initialize git repository
git init

# Configure git (replace with your details)
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### Step 2: Stage and Commit Files
```bash
# Add all files to staging area
git add .

# Check what will be committed
git status

# Commit with descriptive message
git commit -m "Digital Sizing Measurement System - Major Improvements

- Fixed scale factor calculation issues using multiple reference methods
- Improved body proportion accuracy with realistic anatomical ratios
- Updated circumference conversion factors (2.6-2.8 vs π)
- Enhanced measurement validation ranges for real-world values
- Added comprehensive error handling and logging
- Created extensive test suite for measurement validation
- All measurements now within realistic human ranges"
```

### Step 3: Create Remote Repository
1. Go to GitHub (https://github.com) or your preferred git hosting service
2. Click "New Repository" or "+"
3. Name it: `digital-sizing` or `digital-sizing-app`
4. Set it as Public or Private (your choice)
5. Don't initialize with README (we already have one)
6. Copy the repository URL (e.g., `https://github.com/yourusername/digital-sizing.git`)

### Step 4: Connect and Push to Remote
```bash
# Add remote repository (replace URL with yours)
git remote add origin https://github.com/yourusername/digital-sizing.git

# Set main branch
git branch -M main

# Push to remote repository
git push -u origin main
```

## What's Included in This Commit

### Core Application Files:
- `app/` - Main application code with all measurement improvements
- `requirements.txt` - Python dependencies
- `README.md` - Project documentation
- `.gitignore` - Git ignore rules

### Key Improvements Committed:
- **Fixed Measurement System**: Scale factors, circumference calculations, body proportions
- **Enhanced Error Handling**: Type conversion, validation, logging
- **Test Suite**: Comprehensive testing for measurement accuracy
- **Documentation**: Detailed improvement summary and setup guides

### Files Excluded (in .gitignore):
- `__pycache__/` and compiled Python files
- Virtual environment directories
- Upload directories with user images
- Debug and temporary test files
- IDE configuration files

## Verification

After pushing, verify your repository:
1. Visit your repository URL in a browser
2. Check that all files are present
3. Verify the commit message and description
4. Test cloning: `git clone <your-repo-url>`

## Next Steps

1. **Set up GitHub Actions** (optional): Automate testing and deployment
2. **Add collaborators**: Invite team members to contribute
3. **Create branches**: For new features or experiments
4. **Write issues**: Track bugs and feature requests
5. **Documentation**: Update README with deployment instructions

## Troubleshooting

### Common Issues:
1. **Git not recognized**: Install Git and restart terminal
2. **Permission denied**: Set up SSH keys or use HTTPS with token
3. **Push rejected**: Check if repository already has content
4. **Large files**: Use Git LFS for files over 100MB

### Getting Help:
- Git documentation: https://git-scm.com/doc
- GitHub help: https://docs.github.com
- Project issues: Create an issue in your repository

Your digital sizing project with all measurement improvements is now ready for version control and collaboration!
