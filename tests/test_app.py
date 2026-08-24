from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "SecurePipe Lite is running"
    }


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "environment": "development",
        "secret_configured": False,
    }


def test_metrics():
    response = client.get("/metrics")

    assert response.status_code == 200

    data = response.json()

    assert data["environment"] == "development"
    assert isinstance(data["requests_total"], int)
    assert data["requests_total"] >= 0
    assert isinstance(data["uptime_seconds"], (int, float))
    assert data["uptime_seconds"] >= 0