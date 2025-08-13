# Add Git to PATH for current session
# This script adds Git to the PATH environment variable for the current PowerShell session

Write-Host "Adding Git to PATH for current session..." -ForegroundColor Yellow

# Add Git to PATH for current session
$env:PATH += ";C:\Program Files\Git\bin"

# Verify Git is now available
try {
    $gitVersion = git --version 2>$null
    if ($gitVersion) {
        Write-Host "Success: Git is now available: $gitVersion" -ForegroundColor Green
        Write-Host "You can now use 'git' commands directly in this session." -ForegroundColor Green
    } else {
        Write-Host "Error: Failed to add Git to PATH" -ForegroundColor Red
    }
} catch {
    Write-Host "Error: Failed to add Git to PATH" -ForegroundColor Red
}

Write-Host ""
Write-Host "Note: This only affects the current PowerShell session." -ForegroundColor Yellow
Write-Host "To make this permanent, add Git to your system PATH environment variable." -ForegroundColor Yellow
