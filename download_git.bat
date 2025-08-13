@echo off
echo ================================================================
echo GIT INSTALLATION HELPER
echo ================================================================
echo.
echo Git is not installed on your system.
echo.
echo Please follow these steps:
echo.
echo 1. DOWNLOAD GIT:
echo    Opening Git download page in your browser...
echo.
start https://git-scm.com/download/windows
echo.
echo 2. INSTALL GIT:
echo    - Run the downloaded installer
echo    - Accept all default settings (click Next through all screens)
echo    - Click Install and wait for completion
echo    - Click Finish
echo.
echo 3. RESTART:
echo    - Close this command prompt
echo    - Open a new command prompt or PowerShell
echo    - Navigate back to your project directory
echo    - Run: git --version (to verify installation)
echo.
echo 4. SETUP REPOSITORY:
echo    After Git is installed, run: setup_git.bat
echo.
echo ================================================================
echo.
pause
echo.
echo Alternative option: Use GitHub Desktop (easier GUI)
echo Opening GitHub Desktop download page...
start https://desktop.github.com/
echo.
echo GitHub Desktop is a visual Git client that's easier to use
echo for beginners. It includes Git and provides a graphical interface.
echo.
pause
