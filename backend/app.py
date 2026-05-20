"""
NeoTwin — Main FastAPI Application
Production-ready backend for 3D Digital Twin Platform
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

load_dotenv()

# Force early PyTorch import to ensure transformers pipelines register it correctly
import torch

# CORS: read comma-separated origins from env ("*" for open access)
_raw_origins = os.getenv("ALLOWED_ORIGINS", "*")
ALLOWED_ORIGINS = [o.strip() for o in _raw_origins.split(",")]

from api.routes_search import router as search_router
from api.routes_identify import router as identify_router
from api.routes_narrate import router as narrate_router
from api.routes_pipeline import router as pipeline_router
from api.routes_health import router as health_router
from core.config import settings
from core.monitoring import setup_monitoring


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown"""
    print("🚀 NeoTwin Backend Starting...")
    print(f"📊 Monitoring: {settings.ENABLE_MONITORING}")
    print(f"🤖 AI Provider: Gemini 2.0 Flash")
    yield
    print("👋 NeoTwin Backend Shutting Down...")


app = FastAPI(
    title="NeoTwin API",
    description="Production-ready 3D Digital Twin Backend",
    version="1.0.0",
    lifespan=lifespan
)

# CORS — driven by ALLOWED_ORIGINS env var
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security headers
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Restrict in production
)

# Setup monitoring
if settings.ENABLE_MONITORING:
    setup_monitoring(app)

from fastapi.staticfiles import StaticFiles

# Ensure data directory exists and mount it statically to serve reconstruction outputs
os.makedirs("data", exist_ok=True)
app.mount("/data", StaticFiles(directory="data"), name="data")

# Include routers
app.include_router(health_router, prefix="/api/v1", tags=["health"])
app.include_router(search_router, prefix="/api/v1", tags=["search"])
app.include_router(identify_router, prefix="/api/v1", tags=["identify"])
app.include_router(narrate_router, prefix="/api/v1", tags=["narrate"])
app.include_router(pipeline_router, prefix="/api/v1", tags=["pipeline"])


@app.get("/")
async def root():
    return {
        "name": "NeoTwin API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 7860)),
        reload=True
    )
