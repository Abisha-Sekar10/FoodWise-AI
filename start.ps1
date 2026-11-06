# FoodWise AI Startup Script (PowerShell)
Write-Host "=====================================================================" -ForegroundColor Green
Write-Host " FoodWise AI - Smart Food Waste Management & Redistribution Ecosystem" -ForegroundColor Green
Write-Host " MoFPI Problem Statement 26234" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Green

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "`nLaunching FastAPI Backend on http://localhost:8000..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectRoot\backend'; python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

Write-Host "Launching Vite React Frontend on http://localhost:5173..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectRoot\frontend'; npm run dev"

Write-Host "`nAll services active!" -ForegroundColor Green
Write-Host "Frontend:     http://localhost:5173" -ForegroundColor White
Write-Host "Backend API:  http://localhost:8000" -ForegroundColor White
Write-Host "Swagger Docs: http://localhost:8000/docs" -ForegroundColor White
