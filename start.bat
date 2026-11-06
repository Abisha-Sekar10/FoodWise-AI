@echo off
echo =====================================================================
echo  FoodWise AI - Smart Food Waste Reduction ^& Sustainable Redistribution
echo  Ministry of Food Processing Industries (MoFPI) - Problem 26234
echo =====================================================================
echo.
echo Starting Backend (FastAPI on Port 8000)...
start "FoodWise AI Backend" cmd /k "cd backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

echo Starting Frontend (React Vite on Port 5173)...
start "FoodWise AI Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo =====================================================================
echo Application services launched!
echo - Frontend:  http://localhost:5173
echo - Backend API: http://localhost:8000
echo - Swagger Docs: http://localhost:8000/docs
echo =====================================================================
pause
