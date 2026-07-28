@echo off
setlocal enabledelayedexpansion
title Django LAN Server Starter

echo ==========================================================
echo               DJANGO LAN SERVER STARTER
echo ==========================================================
echo.
echo [1] Finding your local IP Address(es)...
echo ----------------------------------------------------------
echo Please use one of the URLs below on your phone or tablet:
for /f "tokens=2 delims=:" %%A in ('ipconfig ^| findstr /i "IPv4"') do (
    set ip=%%A
    rem Trim leading space
    set ip=!ip:~1!
    echo   - http://!ip!:8000/
)
echo ----------------------------------------------------------
echo.
echo IMPORTANT: Make sure your phone or other device is connected
echo to the EXACT SAME Wi-Fi network as this computer.
echo.

rem Check if virtual environment exists and activate it
if exist ".venv\Scripts\activate.bat" (
    echo [2] Activating virtual environment venv...
    call .venv\Scripts\activate.bat
) else (
    echo [2] No virtual environment venv found, using global python...
)

echo.
echo [3] Starting Django server on 0.0.0.0:8000...
echo.
python manage.py runserver 0.0.0.0:8000
pause
