"""Custom exception handlers"""
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status": exc.status_code}
    )

async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "status": 500}
    )
