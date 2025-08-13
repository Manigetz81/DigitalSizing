# Git Installation Script for Windows
# This script downloads and installs Git, then sets up your repository

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "GIT INSTALLATION AND REPOSITORY SETUP" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Host "This script needs to be run as Administrator to install Git." -ForegroundColor Red
    Write-Host "Please:" -ForegroundColor Yellow
    Write-Host "1. Right-click on PowerShell" -ForegroundColor Yellow
    Write-Host "2. Select 'Run as Administrator'" -ForegroundColor Yellow
    Write-Host "3. Navigate to this directory and run the script again" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Or use the manual installation option below." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit
}

# Check if Git is already installed
try {
    $gitVersion = git --version 2>$null
    if ($gitVersion) {
        Write-Host "✓ Git is already installed: $gitVersion" -ForegroundColor Green
        $installGit = $false
    }
} catch {
    Write-Host "Git is not installed. Installing now..." -ForegroundColor Yellow
    $installGit = $true
}

if ($installGit) {
    # Download Git installer
    $gitUrl = "https://github.com/git-for-windows/git/releases/download/v2.45.2.windows.1/Git-2.45.2-64-bit.exe"
    $installerPath = "$env:TEMP\GitInstaller.exe"

    Write-Host "Downloading Git installer..." -ForegroundColor Yellow
    try {
        Invoke-WebRequest -Uri $gitUrl -OutFile $installerPath -UseBasicParsing
        Write-Host "✓ Download completed" -ForegroundColor Green
    } catch {
        Write-Host "✗ Failed to download Git installer" -ForegroundColor Red
        Write-Host "Please install Git manually from: https://git-scm.com/download/windows" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit
    }

    # Install Git silently
    Write-Host "Installing Git..." -ForegroundColor Yellow
    try {
        Start-Process -FilePath $installerPath -ArgumentList "/VERYSILENT /NORESTART /NOCANCEL /SP- /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS /COMPONENTS=`"icons,ext\reg\shellhere,assoc,assoc_sh`"" -Wait
        Write-Host "✓ Git installation completed" -ForegroundColor Green

        # Add Git to PATH for current session
        $env:PATH += ";C:\Program Files\Git\bin"

        # Clean up installer
        Remove-Item $installerPath -ErrorAction SilentlyContinue

    } catch {
        Write-Host "✗ Failed to install Git" -ForegroundColor Red
        Write-Host "Please install Git manually from: https://git-scm.com/download/windows" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit
    }
}

# Wait a moment for Git to be available
Start-Sleep -Seconds 2

# Verify Git installation
try {
    $gitVersion = & "C:\Program Files\Git\bin\git.exe" --version
    Write-Host "✓ Git is now available: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Git was installed but may require a system restart" -ForegroundColor Yellow
    Write-Host "Please restart your computer and then run the repository setup script" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Green
Write-Host "GIT INSTALLATION SUCCESSFUL!" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green

# Now set up the repository
Write-Host ""
Write-Host "Setting up Git repository..." -ForegroundColor Cyan

# Change to script directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Initialize repository
Write-Host "Initializing git repository..." -ForegroundColor Yellow
& "C:\Program Files\Git\bin\git.exe" init

# Configure git
Write-Host ""
$userName = Read-Host "Enter your name for git commits"
& "C:\Program Files\Git\bin\git.exe" config user.name $userName

$userEmail = Read-Host "Enter your email for git commits"
& "C:\Program Files\Git\bin\git.exe" config user.email $userEmail

# Add files and commit
Write-Host ""
Write-Host "Adding files and creating initial commit..." -ForegroundColor Yellow
& "C:\Program Files\Git\bin\git.exe" add .

$commitMessage = "Digital Sizing Measurement System - Initial Commit with Major Improvements

- Implemented accurate scale factor calculation using multiple reference methods
- Fixed body proportion accuracy with realistic anatomical ratios
- Corrected circumference conversion factors (2.6-2.8 vs π)
- Enhanced measurement validation ranges for real-world values
- Added comprehensive error handling and logging
- Created extensive test suite for measurement validation
- All measurements now within realistic human ranges

Technical improvements:
- Scale factor: Multi-method calculation (shoulders/hips/image) with validation
- Circumference: Body-appropriate conversion factors
- Proportions: Accurate head-to-body ratios (7.5:1)
- Validation: Realistic ranges (height: 120-250cm, arm: 40-90cm)
- Error handling: Type conversion and detailed logging

Results: Consistent realistic measurements across test images."

& "C:\Program Files\Git\bin\git.exe" commit -m $commitMessage

Write-Host ""
Write-Host "✓ Repository initialized and initial commit created" -ForegroundColor Green

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "NEXT STEPS" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

Write-Host "1. Create a repository on GitHub/GitLab/Bitbucket" -ForegroundColor White
Write-Host "2. Copy the repository URL" -ForegroundColor White
Write-Host "3. Run these commands in a new PowerShell window:" -ForegroundColor White
Write-Host ""
Write-Host '   git remote add origin <your-repository-url>' -ForegroundColor Gray
Write-Host '   git branch -M main' -ForegroundColor Gray
Write-Host '   git push -u origin main' -ForegroundColor Gray
Write-Host ""
Write-Host "Example:" -ForegroundColor Yellow
Write-Host '   git remote add origin https://github.com/yourusername/digital-sizing.git' -ForegroundColor Gray
Write-Host '   git branch -M main' -ForegroundColor Gray
Write-Host '   git push -u origin main' -ForegroundColor Gray

Write-Host ""
Write-Host "✓ Git is now installed and your project is ready!" -ForegroundColor Green
Read-Host "Press Enter to exit"
