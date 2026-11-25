from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


def test_register_login_and_profile() -> None:
    client = TestClient(app)

    # Adresse unique à chaque exécution du test
    email = f"phase2-{uuid4().hex}@example.com"

    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": "secure-pass-123",
            "full_name": "Phase Two",
        },
    )

    assert response.status_code == 201

    token = response.json()["access_token"]

    profile = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert profile.status_code == 200
    assert profile.json()["email"] == email

    login = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "secure-pass-123",
        },
    )

    assert login.status_code == 200
    assert login.json()["user"]["email"] == email