@echo off
REM Start script for SEO-SWARM Frontend (Windows)

echo Starting SEO-SWARM Frontend...

REM Check if in frontend directory
if not exist "package.json" (
    echo Not in frontend directory. Navigating...
    cd /d "%~dp0"
)

REM Check Python
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python 3 is required but not installed.
    exit /b 1
)

REM Check Node.js
where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Node.js is required but not installed.
    exit /b 1
)

echo Prerequisites OK

REM Backend setup
echo Setting up backend...
cd backend

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

echo Installing backend dependencies...
pip install -q -r requirements.txt

echo Backend ready

REM Start backend in background
echo Starting backend server...
start "SEO-SWARM Backend" cmd /k "venv\Scripts\activate.bat && python main.py"

cd ..

REM Frontend setup
echo Setting up frontend...

if not exist "node_modules" (
    echo Installing frontend dependencies...
    call npm install
)

echo Frontend ready

REM Start frontend
echo Starting frontend dev server...
echo.
echo Dashboard will be available at:
echo   Frontend: http://localhost:5173
echo   Backend:  http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo.
echo Close this window to stop the frontend server
echo Close the backend window to stop the backend server
echo.

call npm run dev

pause
