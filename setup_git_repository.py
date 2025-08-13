#!/usr/bin/env python3
"""
Git Repository Setup and Push Script for Digital Sizing Project
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{description}...")
    print(f"Running: {command}")

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Success!")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
        else:
            print(f"✗ Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"✗ Exception: {e}")
        return False

    return True

def check_git_installed():
    """Check if git is installed."""
    try:
        result = subprocess.run("git --version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Git is installed: {result.stdout.strip()}")
            return True
        else:
            print("✗ Git is not installed")
            return False
    except:
        print("✗ Git is not installed")
        return False

def main():
    """Main function to set up git repository and push code."""

    print("="*60)
    print("DIGITAL SIZING PROJECT - GIT REPOSITORY SETUP")
    print("="*60)

    # Check if git is installed
    if not check_git_installed():
        print("\nPlease install Git first:")
        print("1. Download from: https://git-scm.com/download/windows")
        print("2. Install with default settings")
        print("3. Restart your terminal/command prompt")
        print("4. Run this script again")
        return

    # Change to project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    print(f"\nWorking in directory: {project_dir}")

    # Check if already a git repository
    if os.path.exists('.git'):
        print("\n✓ Already a git repository")
    else:
        # Initialize git repository
        if not run_command("git init", "Initializing git repository"):
            return

    # Configure git user (if not already configured)
    print("\nChecking git configuration...")
    result = subprocess.run("git config user.name", shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        name = input("Enter your name for git commits: ")
        if not run_command(f'git config user.name "{name}"', "Setting git user name"):
            return

    result = subprocess.run("git config user.email", shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        email = input("Enter your email for git commits: ")
        if not run_command(f'git config user.email "{email}"', "Setting git user email"):
            return

    # Add all files to staging
    if not run_command("git add .", "Adding all files to staging area"):
        return

    # Check status
    if not run_command("git status", "Checking repository status"):
        return

    # Commit changes
    commit_message = """
Digital Sizing Measurement System - Major Improvements

- Fixed scale factor calculation issues
- Improved body proportion accuracy
- Updated circumference conversion factors
- Enhanced measurement validation ranges
- Added comprehensive error handling and logging
- Created extensive test suite for validation
- All measurements now within realistic human ranges

Key fixes:
- Scale factor: Multiple reference methods (shoulders, hips, image dimensions)
- Circumference: Realistic conversion factors (2.6-2.8 vs π)
- Body proportions: Accurate anatomical ratios
- Validation: Expanded ranges for real-world measurements
- Error handling: Type conversion and detailed logging

Results: All major measurements (height, shoulder, chest, waist, hip, arm length)
now calculate successfully with realistic values.
"""

    if not run_command(f'git commit -m "{commit_message.strip()}"', "Committing changes"):
        return

    print("\n" + "="*60)
    print("GIT REPOSITORY SETUP COMPLETE!")
    print("="*60)

    print("\nNext steps to push to a remote repository:")
    print("\n1. Create a new repository on GitHub/GitLab/Bitbucket")
    print("2. Copy the repository URL (e.g., https://github.com/username/digital-sizing.git)")
    print("3. Run these commands:")
    print("   git remote add origin <repository-url>")
    print("   git branch -M main")
    print("   git push -u origin main")

    print("\nExample:")
    print("   git remote add origin https://github.com/yourusername/digital-sizing.git")
    print("   git branch -M main")
    print("   git push -u origin main")

    # Ask if user wants to add remote now
    add_remote = input("\nDo you want to add a remote repository URL now? (y/n): ").lower()
    if add_remote == 'y':
        repo_url = input("Enter the repository URL: ")
        if repo_url:
            if not run_command(f"git remote add origin {repo_url}", "Adding remote repository"):
                return

            if not run_command("git branch -M main", "Setting main branch"):
                return

            push_now = input("Push to remote repository now? (y/n): ").lower()
            if push_now == 'y':
                if run_command("git push -u origin main", "Pushing to remote repository"):
                    print("\n🎉 Successfully pushed to remote repository!")
                else:
                    print("\n⚠️  Push failed. You may need to authenticate or check the repository URL.")

    print(f"\n✓ Local git repository is ready in: {project_dir}")
    print("✓ All measurement improvements have been committed")
    print("✓ Ready for collaboration and version control")

if __name__ == "__main__":
    main()
