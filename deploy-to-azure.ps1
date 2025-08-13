# Azure App Service Deployment Script
# Run this script to deploy the Digital Sizing application to Azure

param(
    [Parameter(Mandatory=$true)]
    [string]$ResourceGroupName,
    
    [Parameter(Mandatory=$true)]
    [string]$AppName,
    
    [Parameter(Mandatory=$false)]
    [string]$Location = "East US",
    
    [Parameter(Mandatory=$false)]
    [string]$Sku = "B1"
)

Write-Host "Digital Sizing - Azure Deployment" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

# Check if Azure CLI is installed
try {
    $azVersion = az --version 2>$null
    if ($azVersion) {
        Write-Host "✓ Azure CLI is available" -ForegroundColor Green
    } else {
        Write-Host "✗ Azure CLI is not installed. Please install from https://docs.microsoft.com/en-us/cli/azure/install-azure-cli" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "✗ Azure CLI is not installed. Please install from https://docs.microsoft.com/en-us/cli/azure/install-azure-cli" -ForegroundColor Red
    exit 1
}

# Login to Azure
Write-Host "Logging in to Azure..." -ForegroundColor Yellow
az login

# Create resource group if it doesn't exist
Write-Host "Creating resource group: $ResourceGroupName" -ForegroundColor Yellow
az group create --name $ResourceGroupName --location $Location

# Deploy the ARM template
Write-Host "Deploying Azure App Service..." -ForegroundColor Yellow
az deployment group create `
    --resource-group $ResourceGroupName `
    --template-file "azure-deploy.json" `
    --parameters appName=$AppName location=$Location sku=$Sku

# Configure deployment source
Write-Host "Configuring deployment from local Git..." -ForegroundColor Yellow
az webapp deployment source config-local-git `
    --name $AppName `
    --resource-group $ResourceGroupName

# Get deployment URL
$deploymentUrl = az webapp deployment list-publishing-credentials --name $AppName --resource-group $ResourceGroupName --query "scmUri" --output tsv

Write-Host "✓ Deployment completed!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Add Azure remote: git remote add azure $deploymentUrl" -ForegroundColor White
Write-Host "2. Deploy code: git push azure main" -ForegroundColor White
Write-Host "3. Access your app: https://$AppName.azurewebsites.net" -ForegroundColor White
