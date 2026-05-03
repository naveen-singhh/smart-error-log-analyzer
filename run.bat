@echo off
REM Smart Error Log Analyzer - Windows Batch Script
REM Run this to execute the analyzer on sample logs

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║     Smart Error Log Analyzer - Resume Demo                ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Find Python executable
for /f "delims=" %%i in ('where python 2^>nul') do set PYTHON=%%i

if "!PYTHON!"=="" (
    REM Try python3
    for /f "delims=" %%i in ('where python3 2^>nul') do set PYTHON=%%i
)

if "!PYTHON!"=="" (
    echo Error: Python not found in PATH
    echo Please install Python or add it to your system PATH
    pause
    exit /b 1
)

echo Found Python: !PYTHON!
echo.

REM Install dependencies
echo [1/3] Installing dependencies...
!PYTHON! -m pip install -q click colorama 2>nul
if errorlevel 1 echo Warning: Failed to install dependencies

REM Run analyzer on sample logs
echo [2/3] Analyzing sample logs...
cd /d "%~dp0"
!PYTHON! smart_error_log_analyzer/main.py sample_logs/system.log

echo.
echo [3/3] Reports generated in 'output' folder
echo.
echo Generated files:
if exist "output\system_report.html" echo  ✓ output\system_report.html
if exist "output\system_report.json" echo  ✓ output\system_report.json
echo.
pause
