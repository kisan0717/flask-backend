from app import app

def test_homepage():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json() == {
        "message": "Flask backend is running",
        "status": "success"
    }