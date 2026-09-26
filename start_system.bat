@echo off
title RAINFO - Flash Flood Early Warning System
color 1F

echo ===================================================================
echo     GOVERNMENT OF INDIA - NATIONAL DISASTER MANAGEMENT AUTHORITY
echo         RAINFO: Flash Flood Early Warning System Portal
echo ===================================================================
echo.
echo Starting FastAPI Core Engine...
cd backend
start /B python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
cd ..

timeout /t 2 /nobreak >nul

echo Opening RAINFO Public Portal in browser...
start http://localhost:8000/

echo.
echo ===================================================================
echo   System is LIVE:
echo   Localhost (This Laptop):
echo   - Portal Gateway:        http://localhost:8000/
echo   - Research Methodology:  http://localhost:8000/research
echo   - System Startup Guide:  http://localhost:8000/startup
echo   - Officer Console:       http://localhost:8000/officer
echo   - Public Citizen Portal: http://localhost:8000/user
echo   - Mobile Alert PWA:      http://localhost:8000/mobile  (open on phone)
echo.
echo   Local Wi-Fi / LAN (Share with Presenters & Team):
echo   - Portal Gateway:        http://172.23.183.117:8000/
echo   - Research Methodology:  http://172.23.183.117:8000/research
echo   - Officer Console:       http://172.23.183.117:8000/officer
echo   - Public Citizen Portal: http://172.23.183.117:8000/user
echo ===================================================================
echo.
echo Press any key to stop the server...
pause >nul
taskkill /F /IM python.exe >nul 2>&1
