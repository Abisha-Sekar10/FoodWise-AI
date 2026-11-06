import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import engine, Base
import app.models  # Ensure all models are registered with Base

# Import API routers
from app.api.v1 import auth, admin, kitchen, quality, iot, redistribution, routing, processing, analytics

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="FoodWise AI - Intelligent Food Waste Reduction and Sustainable Redistribution Platform (MoFPI 26234)",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permits local React Vite frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static file mount for food quality images
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Include API v1 Routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication & User Management"])
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["Administrator Dashboard"])
app.include_router(kitchen.router, prefix=f"{settings.API_V1_STR}/kitchen", tags=["Kitchen Demand & Inventory"])
app.include_router(quality.router, prefix=f"{settings.API_V1_STR}/quality", tags=["Smart Quality & Expiry Screening"])
app.include_router(iot.router, prefix=f"{settings.API_V1_STR}/iot", tags=["IoT Cold Storage Telemetry"])
app.include_router(redistribution.router, prefix=f"{settings.API_V1_STR}/redistribution", tags=["Surplus Food Redistribution"])
app.include_router(routing.router, prefix=f"{settings.API_V1_STR}/routing", tags=["AI Route Optimization"])
app.include_router(processing.router, prefix=f"{settings.API_V1_STR}/processing", tags=["Food Processing Industrial Monitoring"])
app.include_router(analytics.router, prefix=f"{settings.API_V1_STR}/analytics", tags=["Sustainability & ESG Analytics"])

@app.get("/")
def root():
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "OPERATIONAL",
        "documentation": "/docs",
        "api_v1": settings.API_V1_STR
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "FoodWise AI Backend",
        "database": "connected"
    }
