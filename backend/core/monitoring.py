"""Monitoring: Prometheus metrics, structured logging"""
from fastapi import FastAPI, Request
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s'
)
logger = logging.getLogger("neotwin")

class MetricsMiddleware:
    def __init__(self, app):
        self.app = app
        self.request_count = 0
        self.request_times = []

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            start = time.time()
            self.request_count += 1
            await self.app(scope, receive, send)
            duration = time.time() - start
            self.request_times.append(duration)
            logger.info(f"Request completed in {duration:.3f}s")

def setup_monitoring(app: FastAPI):
    app.add_middleware(MetricsMiddleware)
    logger.info("Monitoring enabled")
