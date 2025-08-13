# Quick Git Initialization Script
# Run this after installing Git manually

Write-Host "Digital Sizing Project - Git Initialization" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Change to project directory
Set-Location "c:\Mani\Agentic AI\Digital Sizing"

# Check if Git is available
try {
    $gitVersion = git --version 2>$null
    if ($gitVersion) {
        Write-Host "✓ Git is available: $gitVersion" -ForegroundColor Green
    } else {
        Write-Host "✗ Git is not installed. Please install Git first from https://git-scm.com/download/windows" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "✗ Git is not installed. Please install Git first from https://git-scm.com/download/windows" -ForegroundColor Red
    exit 1
}

# Initialize Git repository
Write-Host "Initializing Git repository..." -ForegroundColor Yellow
git init

# Create .gitignore file
Write-Host "Creating .gitignore file..." -ForegroundColor Yellow
$gitignoreContent = @'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/
pip-log.txt
pip-delete-this-directory.txt

# Virtual environments
.venv
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Project specific
app/static/uploads/*.jpg
app/static/uploads/*.jpeg
app/static/uploads/*.png
app/static/uploads/*.gif
!app/static/uploads/.gitkeep

# Logs
*.log

# Environment variables
.env
.env.local

# Temporary files
temp/
tmp/
'@

$gitignoreContent | Out-File -FilePath ".gitignore" -Encoding UTF8

# Configure Git (you'll need to set your own values)
Write-Host "Setting up Git configuration..." -ForegroundColor Yellow
Write-Host "Please enter your Git configuration details:" -ForegroundColor Yellow

$userName = Read-Host "Enter your Git username"
$userEmail = Read-Host "Enter your Git email"

git config --global user.name "$userName"
git config --global user.email "$userEmail"

# Add all files
Write-Host "Adding files to Git..." -ForegroundColor Yellow
git add .

# Create initial commit
Write-Host "Creating initial commit..." -ForegroundColor Yellow
git commit -m "Initial commit: Digital Sizing project setup"

Write-Host "✓ Git repository initialized successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Create a repository on GitHub" -ForegroundColor White
Write-Host "2. Add remote origin: git remote add origin https://github.com/yourusername/digital-sizing.git" -ForegroundColor White
Write-Host "3. Push to GitHub: git push -u origin main" -ForegroundColor White
