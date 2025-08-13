# Azure App Service Deployment Guide

## Overview
This guide will help you deploy the Digital Sizing application to Azure App Service using Python 3.11 and Linux containers.

## Prerequisites

1. **Azure Account**: Active Azure subscription
2. **Azure CLI**: Install from [here](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
3. **Git**: Properly configured with your repository
4. **Python 3.11**: For local testing

## Deployment Methods

### Method 1: Automated Deployment (Recommended)

#### Using PowerShell (Windows):
```powershell
.\deploy-to-azure.ps1 -ResourceGroupName "digital-sizing-rg" -AppName "your-app-name"
```

#### Using Bash (Linux/macOS):
```bash
chmod +x deploy-to-azure.sh
./deploy-to-azure.sh "digital-sizing-rg" "your-app-name"
```

### Method 2: Manual Deployment

#### Step 1: Login to Azure
```bash
az login
```

#### Step 2: Create Resource Group
```bash
az group create --name "digital-sizing-rg" --location "East US"
```

#### Step 3: Deploy ARM Template
```bash
az deployment group create \
    --resource-group "digital-sizing-rg" \
    --template-file "azure-deploy.json" \
    --parameters appName="your-app-name"
```

#### Step 4: Configure Git Deployment
```bash
az webapp deployment source config-local-git \
    --name "your-app-name" \
    --resource-group "digital-sizing-rg"
```

#### Step 5: Get Deployment Credentials
```bash
az webapp deployment list-publishing-credentials \
    --name "your-app-name" \
    --resource-group "digital-sizing-rg"
```

#### Step 6: Deploy Code
```bash
# Add Azure remote
git remote add azure <deployment-url-from-step-5>

# Push to Azure
git push azure main
```

## Configuration Files

### Key Files for Azure Deployment:
- `requirements.txt` - Python dependencies
- `app.py` - WSGI entry point
- `wsgi.py` - Alternative entry point
- `gunicorn.conf.py` - Gunicorn configuration
- `Procfile` - Process definition
- `runtime.txt` - Python version
- `startup.sh` - Startup script
- `.env.production` - Production environment variables

### Important Environment Variables:
- `SECRET_KEY` - Flask secret key (auto-generated)
- `WEBSITES_PORT` - Port for Azure (8000)
- `FLASK_ENV` - Set to "production"
- `SCM_DO_BUILD_DURING_DEPLOYMENT` - Enable build

## Application Structure

```
digital-sizing/
├── app/                    # Main application
│   ├── main.py            # Flask application
│   ├── models/            # ML models
│   ├── utils/             # Utilities
│   ├── templates/         # HTML templates
│   └── static/            # Static files
├── requirements.txt       # Dependencies
├── app.py                 # WSGI entry point
├── gunicorn.conf.py      # Gunicorn config
├── azure-deploy.json     # ARM template
└── deploy-to-azure.ps1   # Deployment script
```

## Performance Considerations

### Recommended SKUs:
- **Development**: F1 (Free tier)
- **Testing**: B1 (Basic)
- **Production**: P1v2 or higher (Premium)

### Optimizations:
1. Uses `opencv-python-headless` for smaller size
2. Gunicorn for production WSGI server
3. Proper error handling and logging
4. Efficient file handling for uploads

## Monitoring and Logs

### View Application Logs:
```bash
az webapp log tail --name "your-app-name" --resource-group "digital-sizing-rg"
```

### Enable Application Insights:
```bash
az monitor app-insights component create \
    --app "your-app-name-insights" \
    --location "East US" \
    --resource-group "digital-sizing-rg"
```

## Troubleshooting

### Common Issues:

1. **Build Failures**:
   - Check Python version in `runtime.txt`
   - Verify all dependencies in `requirements.txt`
   - Check build logs in Azure portal

2. **Startup Issues**:
   - Verify `app.py` entry point
   - Check gunicorn configuration
   - Review application logs

3. **Memory Issues**:
   - Upgrade to higher SKU (B2, S1, or P1v2)
   - Optimize image processing
   - Implement proper garbage collection

4. **File Upload Issues**:
   - Check upload folder permissions
   - Verify file size limits
   - Ensure proper cleanup

### Debug Commands:
```bash
# Check app status
az webapp show --name "your-app-name" --resource-group "digital-sizing-rg"

# Restart app
az webapp restart --name "your-app-name" --resource-group "digital-sizing-rg"

# View configuration
az webapp config show --name "your-app-name" --resource-group "digital-sizing-rg"
```

## Security Best Practices

1. **Environment Variables**: Store sensitive data in App Settings
2. **HTTPS**: Enabled by default on Azure App Service
3. **Authentication**: Consider Azure AD integration
4. **File Validation**: Implemented in the application
5. **Rate Limiting**: Consider implementing for production

## Scaling

### Horizontal Scaling:
```bash
az appservice plan update \
    --name "your-app-plan" \
    --resource-group "digital-sizing-rg" \
    --number-of-workers 2
```

### Vertical Scaling:
```bash
az appservice plan update \
    --name "your-app-plan" \
    --resource-group "digital-sizing-rg" \
    --sku P1v2
```

## Post-Deployment

1. **Test the Application**: Visit `https://your-app-name.azurewebsites.net`
2. **Upload a Test Image**: Verify image processing works
3. **Monitor Performance**: Check response times and errors
4. **Set up Alerts**: Configure monitoring alerts
5. **Custom Domain**: Add your domain if needed

## Support

For issues related to:
- **Azure Service**: Check Azure documentation and support
- **Application Code**: Review application logs and error messages
- **Dependencies**: Verify all packages are compatible with Python 3.11

## Cost Optimization

1. **Use Free Tier** for development (F1)
2. **Scale Down** during off-hours
3. **Monitor Usage** with Azure Cost Management
4. **Auto-scale** based on demand
