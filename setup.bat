@echo off
REM Resume Parser - Quick Start Script for Windows

echo.
echo ========================================
echo Resume Parser Using AI - Quick Start
echo ========================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed. Please install it from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed. Please install it from https://www.python.org/
    pause
    exit /b 1
)

echo [INFO] Node.js and Python detected successfully
echo.

REM Check if .env file exists in backend
if not exist "backend\.env" (
    echo [WARNING] backend\.env file not found!
    echo Please create backend\.env with required variables:
    echo   - MONGODB_URI
    echo.
)

echo [STEP 1] Installing Backend Dependencies...
cd backend
call npm install
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install backend dependencies
    pause
    exit /b 1
)
cd ..
echo [OK] Backend dependencies installed
echo.

echo [STEP 2] Installing Frontend Dependencies...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install frontend dependencies
    pause
    exit /b 1
)
cd ..
echo [OK] Frontend dependencies installed
echo.

echo [STEP 3] Setting Up Python Virtual Environment...
cd Resume_Parser
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate.bat
pip install -r requirement.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install Python dependencies
    pause
    exit /b 1
)
echo [OK] Python dependencies installed
cd ..
echo.

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the application, open 3 terminal windows and run:
echo.
echo Terminal 1 (Backend):
echo   cd backend
echo   npm start
echo.
echo Terminal 2 (Python API):
echo   cd Resume_Parser
echo   venv\Scripts\activate
echo   python main.py
echo.
echo Terminal 3 (Frontend):
echo   cd frontend
echo   npm run dev
echo.
echo Then open http://localhost:5173 in your browser
echo.
echo For detailed instructions, see SETUP.md
echo.
pause
