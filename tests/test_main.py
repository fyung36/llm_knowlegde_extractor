from fastapi.testclient import TestClient
from src.knowledge_extractor import route
client = TestClient(src)

def test_analyze_empty_text():
    response = client.post("/analyze", json={"text": ""})
    assert response.status_code == 400
    assert response.json()["detail"] == "Input text cannot be empty."

def test_analyze_too_short_text():
    response = client.post("/analyze", json={"text": "Hi there."})
    assert response.status_code == 422
    assert "too short" in response.json()["detail"]

def test_search_missing_query_param():
    response = client.get("/search")
    assert response.status_code == 422

def test_search_no_results():
    response = client.get("/search?topic=nonexistent")
    assert response.status_code == 404
