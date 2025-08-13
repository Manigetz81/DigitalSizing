# Manual Git Installation Guide

## Step 1: Download and Install Git

1. **Download Git:**
   - Go to: https://git-scm.com/download/windows
   - Click "64-bit Git for Windows Setup" (latest version)
   - Save the file to your Downloads folder

2. **Install Git:**
   - Run the downloaded installer (.exe file)
   - Accept all default settings (just click "Next" through all screens)
   - Click "Install" and wait for completion
   - Click "Finish"

3. **Restart PowerShell/Command Prompt:**
   - Close any open terminal windows
   - Open a new PowerShell or Command Prompt
   - Navigate back to your project directory

## Step 2: Verify Git Installation

Open PowerShell and run:
```powershell
git --version
```
You should see something like: `git version 2.45.2.windows.1`

## Step 3: Set Up Your Repository

Once Git is installed, run these commands one by one:

```powershell
# Navigate to your project directory
cd "c:\Mani\Agentic AI\Digital Sizing"

# Initialize git repository
git init

# Configure git with your information
git config user.name "Your Full Name"
git config user.email "your.email@example.com"

# Add all files to staging
git add .

# Create initial commit
git commit -m "Digital Sizing Measurement System - Initial Commit

- Implemented accurate scale factor calculation
- Fixed body proportion accuracy
- Corrected circumference conversion factors
- Enhanced measurement validation ranges
- Added comprehensive error handling and logging
- All measurements now within realistic human ranges"
```

## Step 4: Push to Remote Repository

1. **Create a new repository:**
   - Go to GitHub.com (create account if needed)
   - Click "New" or "+" to create new repository
   - Name it: `digital-sizing`
   - Keep it Public or make it Private
   - Don't initialize with README (we have one)
   - Click "Create repository"

2. **Connect and push:**
   Replace `yourusername` and `your-repo-name` with your actual values:
   ```powershell
   git remote add origin https://github.com/yourusername/digital-sizing.git
   git branch -M main
   git push -u origin main
   ```

## Alternative: Use GitHub Desktop (Easiest)

If you prefer a visual interface:

1. **Download GitHub Desktop:**
   - Go to: https://desktop.github.com/
   - Download and install

2. **Set up repository:**
   - Open GitHub Desktop
   - File → Add Local Repository
   - Choose your project folder
   - Create repository when prompted
   - Publish to GitHub

## Troubleshooting

**If git command still not found after installation:**
1. Restart your computer
2. Or manually add to PATH: `C:\Program Files\Git\bin`

**If you get permission errors:**
1. Run PowerShell as Administrator
2. Or use HTTPS authentication instead of SSH

Your digital sizing project will then be available on GitHub for sharing and collaboration!
