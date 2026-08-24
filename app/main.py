import os

from fastapi import FastAPI

app = FastAPI()

APP_ENV = os.getenv("APP_ENV", "development")
APP_SECRET = os.getenv("APP_SECRET")


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