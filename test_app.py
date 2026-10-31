from app import app
from config import HOME_MESSAGE

def test_homepage():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json() == {
        "message": HOME_MESSAGE,
        "status": "success"
    }

def test_health():
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {
        "status": "healthy"
    }