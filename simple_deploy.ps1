# Simple Azure Deployment Helper
# Since your Azure App Service (CTS-VibeAppce41212-4) is already configured,
# this script helps you deploy quickly

Write-Host "Digital Sizing - Simple Deployment Helper" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

$AppName = "CTS-VibeAppce41212-4"
$AppUrl = "https://$AppName.azurewebsites.net"
$GitHubActionsUrl = "https://github.com/Manigetz81/DigitalSizing/actions"

Write-Host ""
Write-Host "✅ Your Azure App Service is already configured!" -ForegroundColor Green
Write-Host "   App Name: $AppName" -ForegroundColor White
Write-Host "   App URL: $AppUrl" -ForegroundColor Cyan
Write-Host "   GitHub Actions: $GitHubActionsUrl" -ForegroundColor White

Write-Host ""
Write-Host "🚀 Deployment Status:" -ForegroundColor Yellow

# Check if we have any uncommitted changes
$gitStatus = git status --porcelain 2>$null
if ($gitStatus) {
    Write-Host "⚠️  You have uncommitted changes. Committing now..." -ForegroundColor Yellow
    git add .
    git commit -m "chore: Auto-commit for deployment"
    git push origin main
    Write-Host "✅ Changes committed and pushed" -ForegroundColor Green
} else {
    Write-Host "✅ All changes are already committed" -ForegroundColor Green
}

Write-Host ""
Write-Host "📋 Your deployment is automatic via GitHub Actions!" -ForegroundColor Cyan
Write-Host "   • Every push to 'main' branch triggers deployment" -ForegroundColor White
Write-Host "   • GitHub Actions builds and deploys your app" -ForegroundColor White
Write-Host "   • No manual Azure CLI setup required!" -ForegroundColor White

Write-Host ""
Write-Host "🔍 To monitor your deployment:" -ForegroundColor Yellow
Write-Host "1. Visit: $GitHubActionsUrl" -ForegroundColor White
Write-Host "2. Look for the latest 'Build and deploy Python app' workflow" -ForegroundColor White
Write-Host "3. Check the build and deploy progress" -ForegroundColor White

Write-Host ""
Write-Host "🌐 To test your application:" -ForegroundColor Yellow
Write-Host "1. Wait for deployment to complete (usually 5-10 minutes)" -ForegroundColor White
Write-Host "2. Visit: $AppUrl" -ForegroundColor Cyan
Write-Host "3. Try uploading an image to test the functionality" -ForegroundColor White

Write-Host ""
Write-Host "🔧 Quick Troubleshooting:" -ForegroundColor Yellow
Write-Host "• If deployment fails, check GitHub Actions logs" -ForegroundColor White
Write-Host "• If app doesn't load, wait a few more minutes (startup can be slow)" -ForegroundColor White
Write-Host "• For errors, check app logs in Azure portal" -ForegroundColor White

Write-Host ""
$response = Read-Host "Would you like to open the GitHub Actions page to monitor deployment? (y/n)"
if ($response -eq 'y' -or $response -eq 'Y') {
    Start-Process $GitHubActionsUrl
}

$response = Read-Host "Would you like to open your app URL to test when ready? (y/n)"
if ($response -eq 'y' -or $response -eq 'Y') {
    Start-Process $AppUrl
}

Write-Host ""
Write-Host "✅ Deployment initiated! Check GitHub Actions for progress." -ForegroundColor Green
