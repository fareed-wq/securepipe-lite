import json
import logging
import os
import time
from threading import Lock

from fastapi import FastAPI, Request

app = FastAPI()

APP_ENV = os.getenv("APP_ENV", "development")
APP_SECRET = os.getenv("APP_SECRET")

START_TIME = time.monotonic()
REQUEST_COUNT = 0
REQUEST_COUNT_LOCK = Lock()

logger = logging.getLogger("securepipe")
logging.basicConfig(level=logging.INFO)


@app.middleware("http")
async def request_logging(request: Request, call_next):
    global REQUEST_COUNT

    start_time = time.perf_counter()

    try:
        response = await call_next(request)
        status_code = response.status_code
    except Exception:
        status_code = 500
        raise
    finally:
        duration_ms = round(
            (time.perf_counter() - start_time) * 1000,
            2,
        )

        with REQUEST_COUNT_LOCK:
            REQUEST_COUNT += 1

        log_entry = {
            "event": "http_request",
            "method": request.method,
            "path": request.url.path,
            "status_code": status_code,
            "duration_ms": duration_ms,
            "environment": APP_ENV,
        }

        logger.info(json.dumps(log_entry))

    return response


@app.get("/")
def home():
    return {"message": "SecurePipe Lite is running"}


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "environment": APP_ENV,
        "secret_configured": bool(APP_SECRET),
    }


@app.get("/metrics")
def metrics():
    with REQUEST_COUNT_LOCK:
        requests_total = REQUEST_COUNT

    uptime_seconds = round(time.monotonic() - START_TIME, 2)

    return {
        "requests_total": requests_total,
        "uptime_seconds": uptime_seconds,
        "environment": APP_ENV,
    }