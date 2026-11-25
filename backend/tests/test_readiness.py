from fastapi.testclient import TestClient
from app.main import app


def test_readiness_endpoint() -> None:
    response = TestClient(app).get("/health/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"

