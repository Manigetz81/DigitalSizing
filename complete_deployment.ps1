# Complete Azure Deployment Script
# This script will install Azure CLI and deploy the Digital Sizing application

param(
    [Parameter(Mandatory=$false)]
    [string]$AppName = "CTS-VibeAppce41212-4",
    
    [Parameter(Mandatory=$false)]
    [string]$ResourceGroupName = "digital-sizing-rg",
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipAzureCliInstall = $false
)

Write-Host "Digital Sizing - Complete Azure Deployment" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Function to install Azure CLI
function Install-AzureCLI {
    Write-Host "Installing Azure CLI..." -ForegroundColor Yellow
    
    try {
        # Download and install Azure CLI
        $ProgressPreference = 'SilentlyContinue'
        Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\AzureCLI.msi
        Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'
        Remove-Item .\AzureCLI.msi
        
        # Refresh environment variables
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        
        Write-Host "✅ Azure CLI installed successfully!" -ForegroundColor Green
        Write-Host "⚠️  Please restart your PowerShell session and run this script again." -ForegroundColor Yellow
        return $false
    } catch {
        Write-Host "❌ Failed to install Azure CLI: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "Please install manually from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-windows" -ForegroundColor Yellow
        return $false
    }
}

# Check if Azure CLI is available
if (-not $SkipAzureCliInstall) {
    try {
        $azVersion = az --version 2>$null
        if ($azVersion) {
            Write-Host "✅ Azure CLI is available" -ForegroundColor Green
        } else {
            $installed = Install-AzureCLI
            if (-not $installed) { exit 1 }
        }
    } catch {
        $installed = Install-AzureCLI
        if (-not $installed) { exit 1 }
    }
}

Write-Host "Starting deployment process..." -ForegroundColor Yellow

# Login to Azure
Write-Host "Logging in to Azure..." -ForegroundColor Yellow
Write-Host "A browser window will open for authentication." -ForegroundColor Cyan
try {
    az login
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Azure login failed" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Successfully logged in to Azure" -ForegroundColor Green
} catch {
    Write-Host "❌ Azure login failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Check if the app service exists
Write-Host "Checking Azure App Service: $AppName" -ForegroundColor Yellow
try {
    $appInfo = az webapp show --name $AppName --resource-group $ResourceGroupName 2>$null | ConvertFrom-Json
    if ($appInfo) {
        Write-Host "✅ Found existing App Service: $AppName" -ForegroundColor Green
        Write-Host "   Resource Group: $($appInfo.resourceGroup)" -ForegroundColor White
        Write-Host "   Location: $($appInfo.location)" -ForegroundColor White
        Write-Host "   Default Hostname: $($appInfo.defaultHostName)" -ForegroundColor White
        
        $appUrl = "https://$($appInfo.defaultHostName)"
        Write-Host "   App URL: $appUrl" -ForegroundColor Cyan
    } else {
        Write-Host "❌ App Service '$AppName' not found in resource group '$ResourceGroupName'" -ForegroundColor Red
        Write-Host "Creating new App Service..." -ForegroundColor Yellow
        
        # Create resource group if it doesn't exist
        az group create --name $ResourceGroupName --location "East US"
        
        # Create App Service Plan
        az appservice plan create --name "$AppName-plan" --resource-group $ResourceGroupName --sku B1 --is-linux
        
        # Create App Service
        az webapp create --name $AppName --resource-group $ResourceGroupName --plan "$AppName-plan" --runtime "PYTHON|3.11"
        
        $appInfo = az webapp show --name $AppName --resource-group $ResourceGroupName | ConvertFrom-Json
        $appUrl = "https://$($appInfo.defaultHostName)"
    }
} catch {
    Write-Host "❌ Error checking App Service: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Configure App Service settings
Write-Host "Configuring App Service settings..." -ForegroundColor Yellow
try {
    az webapp config appsettings set --name $AppName --resource-group $ResourceGroupName --settings `
        WEBSITES_PORT=8000 `
        SCM_DO_BUILD_DURING_DEPLOYMENT=true `
        FLASK_ENV=production `
        SECRET_KEY="$(New-Guid)" `
        WEBSITES_CONTAINER_START_TIME_LIMIT=1800
    
    Write-Host "✅ App Service settings configured" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Warning: Could not set all app settings: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Configure deployment from GitHub (if not already configured)
Write-Host "Checking deployment configuration..." -ForegroundColor Yellow
try {
    $sourceControl = az webapp deployment source show --name $AppName --resource-group $ResourceGroupName 2>$null | ConvertFrom-Json
    if ($sourceControl -and $sourceControl.repoUrl) {
        Write-Host "✅ Deployment already configured from: $($sourceControl.repoUrl)" -ForegroundColor Green
    } else {
        Write-Host "GitHub Actions deployment will be used automatically" -ForegroundColor Cyan
    }
} catch {
    Write-Host "ℹ️  Deployment will be handled by GitHub Actions" -ForegroundColor Blue
}

# Commit and push any pending changes
Write-Host "Ensuring all changes are pushed to GitHub..." -ForegroundColor Yellow
try {
    $gitStatus = git status --porcelain 2>$null
    if ($gitStatus) {
        Write-Host "Adding and committing pending changes..." -ForegroundColor Yellow
        git add .
        git commit -m "chore: Auto-commit before deployment"
    }
    
    git push origin main
    Write-Host "✅ Code pushed to GitHub" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Warning: Could not push to GitHub: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 Deployment process completed!" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Deployment Summary:" -ForegroundColor Cyan
Write-Host "   • App Service: $AppName" -ForegroundColor White
Write-Host "   • Resource Group: $ResourceGroupName" -ForegroundColor White
Write-Host "   • App URL: $appUrl" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 Next Steps:" -ForegroundColor Yellow
Write-Host "1. GitHub Actions will automatically deploy your code" -ForegroundColor White
Write-Host "2. Check deployment status at: https://github.com/Manigetz81/DigitalSizing/actions" -ForegroundColor White
Write-Host "3. Test your app at: $appUrl" -ForegroundColor White
Write-Host "4. Monitor logs: az webapp log tail --name $AppName --resource-group $ResourceGroupName" -ForegroundColor White
Write-Host ""
Write-Host "⏳ Deployment typically takes 5-15 minutes via GitHub Actions" -ForegroundColor Cyan

# Test deployment after a short wait
Write-Host ""
$response = Read-Host "Would you like to test the deployment now? (y/n)"
if ($response -eq 'y' -or $response -eq 'Y') {
    Write-Host "Testing deployment in 30 seconds..." -ForegroundColor Yellow
    Start-Sleep -Seconds 30
    
    try {
        python test_deployment.py $appUrl
    } catch {
        Write-Host "⚠️  Could not run deployment test. You can test manually at: $appUrl" -ForegroundColor Yellow
    }
}
