"""API Routes: Health & Metrics"""
from fastapi import APIRouter
from pydantic import BaseModel
import psutil
import torch

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    version: str
    gpu_available: bool
    gpu_memory_mb: float = 0
    cpu_percent: float
    memory_percent: float

@router.get("/health", response_model=HealthResponse)
async def health_check():
    gpu_available = torch.cuda.is_available()
    gpu_memory = 0
    if gpu_available:
        gpu_memory = torch.cuda.memory_allocated() / (1024 * 1024)
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        gpu_available=gpu_available,
        gpu_memory_mb=round(gpu_memory, 2),
        cpu_percent=psutil.cpu_percent(),
        memory_percent=psutil.virtual_memory().percent
    )

@router.get("/metrics")
async def get_metrics():
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory()._asdict(),
        "gpu": {
            "available": torch.cuda.is_available(),
            "device_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
            "device_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "N/A"
        }
    }
