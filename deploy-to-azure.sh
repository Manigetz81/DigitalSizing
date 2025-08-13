#!/bin/bash

# Azure App Service Deployment Script for Linux/macOS
# Usage: ./deploy-to-azure.sh <resource-group-name> <app-name> [location] [sku]

RESOURCE_GROUP_NAME=$1
APP_NAME=$2
LOCATION=${3:-"East US"}
SKU=${4:-"B1"}

if [ -z "$RESOURCE_GROUP_NAME" ] || [ -z "$APP_NAME" ]; then
    echo "Usage: $0 <resource-group-name> <app-name> [location] [sku]"
    echo "Example: $0 my-resource-group digital-sizing-app"
    exit 1
fi

echo "Digital Sizing - Azure Deployment"
echo "================================="

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI is not installed. Please install from https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi

echo "✅ Azure CLI is available"

# Login to Azure
echo "Logging in to Azure..."
az login

# Create resource group if it doesn't exist
echo "Creating resource group: $RESOURCE_GROUP_NAME"
az group create --name "$RESOURCE_GROUP_NAME" --location "$LOCATION"

# Deploy the ARM template
echo "Deploying Azure App Service..."
az deployment group create \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --template-file "azure-deploy.json" \
    --parameters appName="$APP_NAME" location="$LOCATION" sku="$SKU"

# Configure deployment source
echo "Configuring deployment from local Git..."
az webapp deployment source config-local-git \
    --name "$APP_NAME" \
    --resource-group "$RESOURCE_GROUP_NAME"

# Get deployment URL
DEPLOYMENT_URL=$(az webapp deployment list-publishing-credentials --name "$APP_NAME" --resource-group "$RESOURCE_GROUP_NAME" --query "scmUri" --output tsv)

echo "✅ Deployment completed!"
echo ""
echo "Next steps:"
echo "1. Add Azure remote: git remote add azure $DEPLOYMENT_URL"
echo "2. Deploy code: git push azure main"
echo "3. Access your app: https://$APP_NAME.azurewebsites.net"
