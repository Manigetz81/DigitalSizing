# Digital Sizing - Quick Deployment
Write-Host "Digital Sizing - Quick Deployment" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

$AppName = "CTS-VibeAppce41212-4"
$AppUrl = "https://$AppName.azurewebsites.net"
$GitHubActionsUrl = "https://github.com/Manigetz81/DigitalSizing/actions"

Write-Host ""
Write-Host "App Name: $AppName" -ForegroundColor White
Write-Host "App URL: $AppUrl" -ForegroundColor Cyan
Write-Host "GitHub Actions: $GitHubActionsUrl" -ForegroundColor White

Write-Host ""
Write-Host "Checking git status..." -ForegroundColor Yellow
$gitStatus = git status --porcelain 2>$null
if ($gitStatus) {
    Write-Host "Committing changes..." -ForegroundColor Yellow
    git add .
    git commit -m "chore: Auto-commit for deployment"
    git push origin main
    Write-Host "Changes pushed to trigger deployment" -ForegroundColor Green
} else {
    Write-Host "All changes already committed" -ForegroundColor Green
}

Write-Host ""
Write-Host "Deployment will happen automatically via GitHub Actions" -ForegroundColor Cyan
Write-Host "Visit $GitHubActionsUrl to monitor progress" -ForegroundColor White
Write-Host ""
Write-Host "Your app will be available at: $AppUrl" -ForegroundColor Cyan
