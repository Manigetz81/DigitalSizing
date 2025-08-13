@echo off
echo ================================================================
echo DIGITAL SIZING PROJECT - GIT REPOSITORY SETUP (Windows)
echo ================================================================

REM Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Git is not installed or not in PATH
    echo.
    echo Please install Git first:
    echo 1. Download from: https://git-scm.com/download/windows
    echo 2. Install with default settings
    echo 3. Restart your command prompt
    echo 4. Run this script again
    echo.
    pause
    exit /b 1
)

echo Git is installed and available
echo.

REM Change to script directory
cd /d "%~dp0"
echo Working in directory: %CD%

REM Initialize git repository if not already done
if not exist ".git" (
    echo Initializing git repository...
    git init
    if %errorlevel% neq 0 (
        echo Failed to initialize git repository
        pause
        exit /b 1
    )
    echo Repository initialized successfully
) else (
    echo Already a git repository
)

REM Check git configuration
git config user.name >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    set /p username="Enter your name for git commits: "
    git config user.name "!username!"
)

git config user.email >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    set /p useremail="Enter your email for git commits: "
    git config user.email "!useremail!"
)

echo.
echo Current git configuration:
git config user.name
git config user.email

echo.
echo Adding all files to staging area...
git add .

echo.
echo Repository status:
git status

echo.
echo Committing changes...
git commit -m "Digital Sizing Measurement System - Major Improvements

- Fixed scale factor calculation issues using multiple reference methods
- Improved body proportion accuracy with realistic anatomical ratios
- Updated circumference conversion factors (2.6-2.8 vs π)
- Enhanced measurement validation ranges for real-world values
- Added comprehensive error handling and logging
- Created extensive test suite for measurement validation
- All measurements now within realistic human ranges

Key technical improvements:
- Scale factor: Shoulder/hip/image-based calculation with validation
- Circumference: Body-appropriate conversion factors instead of π
- Proportions: Accurate head-to-body ratios (7.5:1 vs 8:1)
- Validation: Expanded ranges (height: 120-250cm, arm: 40-90cm)
- Error handling: Type conversion and detailed debug logging

Results: Measurements like shoulder width (40cm), chest (95cm),
arm length (63cm) now consistently realistic across test images."

if %errorlevel% neq 0 (
    echo Failed to commit changes
    pause
    exit /b 1
)

echo.
echo ================================================================
echo COMMIT SUCCESSFUL!
echo ================================================================

echo.
echo Next steps to push to a remote repository:
echo.
echo 1. Create a new repository on GitHub/GitLab/Bitbucket
echo 2. Copy the repository URL
echo 3. Run these commands:
echo    git remote add origin ^<repository-url^>
echo    git branch -M main
echo    git push -u origin main
echo.
echo Example:
echo    git remote add origin https://github.com/yourusername/digital-sizing.git
echo    git branch -M main
echo    git push -u origin main

echo.
choice /c YN /m "Do you want to add a remote repository URL now?"
if %errorlevel%==1 (
    echo.
    set /p repourl="Enter the repository URL: "
    if not "!repourl!"=="" (
        echo Adding remote repository...
        git remote add origin !repourl!
        if %errorlevel% neq 0 (
            echo Failed to add remote repository
        ) else (
            echo Setting main branch...
            git branch -M main
            echo.
            choice /c YN /m "Push to remote repository now?"
            if %errorlevel%==1 (
                echo Pushing to remote repository...
                git push -u origin main
                if %errorlevel%==0 (
                    echo.
                    echo 🎉 Successfully pushed to remote repository!
                ) else (
                    echo.
                    echo ⚠️  Push failed. You may need to authenticate or check the repository URL.
                )
            )
        )
    )
)

echo.
echo ✓ Local git repository is ready
echo ✓ All measurement improvements have been committed
echo ✓ Ready for collaboration and version control
echo.
pause
