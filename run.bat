@echo off
REM Resume Parser - starts Backend, AI service and Frontend in separate terminals

set "ROOT=%~dp0"

echo.
echo ========================================
echo  Resume Parser Using AI - Starting
echo ========================================
echo.

where node >nul 2>nul || (echo [ERROR] Node.js is not installed. & pause & exit /b 1)
where python >nul 2>nul || (echo [ERROR] Python is not installed. & pause & exit /b 1)

if not exist "%ROOT%backend\node_modules" (
    echo [ERROR] Backend dependencies missing. Run setup.bat first.
    pause
    exit /b 1
)
if not exist "%ROOT%frontend\node_modules" (
    echo [ERROR] Frontend dependencies missing. Run setup.bat first.
    pause
    exit /b 1
)
if not exist "%ROOT%backend\.env" (
    echo [WARNING] backend\.env not found. The backend needs MONGODB_URI.
)

echo [1/3] Starting Backend  (http://localhost:3000)
start "Backend - 3000" /D "%ROOT%backend" cmd /k "npm start"

echo [2/3] Starting AI service (http://localhost:5001)
if exist "%ROOT%Resume_Parser\venv\Scripts\activate.bat" (
    start "AI Service - 5001" /D "%ROOT%Resume_Parser" cmd /k "call venv\Scripts\activate.bat && python main.py"
) else (
    start "AI Service - 5001" /D "%ROOT%Resume_Parser" cmd /k "python main.py"
)

echo [3/3] Starting Frontend (http://localhost:5173)
start "Frontend - 5173" /D "%ROOT%frontend" cmd /k "npm run dev"

echo.
echo Waiting for the frontend to start...
timeout /t 8 /nobreak >nul

start "" "http://localhost:5173"

echo.
echo All services started. Close each terminal window to stop its service.
echo (MongoDB must be running separately, or use a MongoDB Atlas URI.)
echo.
