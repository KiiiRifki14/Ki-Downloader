from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_analyze_endpoint_missing_url():
    response = client.post("/api/analyze", json={})
    assert response.status_code == 422

def test_analyze_invalid_url():
    response = client.post("/api/analyze", json={"url": "invalid-url"})
    assert response.status_code == 400
