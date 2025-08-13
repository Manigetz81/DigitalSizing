Write-Host "Digital Sizing Project - Git Initialization" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Check if Git is available
$gitVersion = git --version 2>$null
if ($gitVersion) {
    Write-Host "✓ Git is available: $gitVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Git is not installed" -ForegroundColor Red
    exit 1
}

# Check if already a git repository
if (Test-Path ".git") {
    Write-Host "✓ Git repository already exists" -ForegroundColor Yellow
} else {
    # Initialize Git repository
    Write-Host "Initializing Git repository..." -ForegroundColor Yellow
    git init
}

# Create .gitignore file if it doesn't exist
if (-not (Test-Path ".gitignore")) {
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
}

# Configure Git if not already configured
$userName = git config --global user.name 2>$null
$userEmail = git config --global user.email 2>$null

if (-not $userName) {
    $userName = Read-Host "Enter your Git username"
    git config --global user.name "$userName"
}

if (-not $userEmail) {
    $userEmail = Read-Host "Enter your Git email"
    git config --global user.email "$userEmail"
}

Write-Host "Git configuration:" -ForegroundColor Yellow
Write-Host "  Name: $userName" -ForegroundColor White
Write-Host "  Email: $userEmail" -ForegroundColor White

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
