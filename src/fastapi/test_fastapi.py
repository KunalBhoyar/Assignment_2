from fastapi.testclient import TestClient
from main import app
from user_auth import AuthHandler


client = TestClient(app)
auth_handler = AuthHandler()


def get_token():
    token=auth_handler.encode_token("fake_username")
    return token


def test_read_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "connected"}
    
def test_fetch_url_goes():
    response = client.get(
        "/fetch_url_goes",
        params={"year": 2022, "month": 2, "date": 24},
        headers={"Authorization": get_token()}
    )
    assert response.status_code == 403

def test_register():
    # register a new user
    response = client.post(
        "/register",
        json={"username": "testuser", "password": "testpassword"}
    )
    # try to register the same user again (should fail)
    response = client.post(
        "/register",
        json={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Username is taken"}

def test_login():
    # login with valid credentials
    response = client.post(
        "/login",
        json={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "token" in response.json()

    # login with invalid credentials
    response = client.post(
        "/login",
        json={"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid username and/or password"}