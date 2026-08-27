from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_index_page_returns_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "Ki.Downloader" in response.text

def test_embed_page_returns_html():
    response = client.get("/embed")
    assert response.status_code == 200
    assert "Video Downloader Widget" in response.text
