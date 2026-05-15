"""Security: Rate limiting, API key validation"""
from fastapi import Request, HTTPException
from collections import defaultdict
import time
from core.config import settings

rate_limit_store = defaultdict(list)

def check_rate_limit(client_ip: str) -> bool:
    if not settings.RATE_LIMIT_ENABLED:
        return True
    now = time.time()
    minute_ago = now - 60
    rate_limit_store[client_ip] = [
        t for t in rate_limit_store[client_ip] if t > minute_ago
    ]
    if len(rate_limit_store[client_ip]) >= settings.RATE_LIMIT_PER_MINUTE:
        return False
    rate_limit_store[client_ip].append(now)
    return True

def validate_api_key(request: Request):
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        raise HTTPException(status_code=401, detail="API key required")
    return api_key
