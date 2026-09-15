from app.core.security import hash_password
from app.models.user import User, UserRole


def test_admin_access_admin_endpoint(client, db_session):
    admin_user = User(
        email="admin@example.com",
        hashed_password=hash_password("adminpass123"),
        role=UserRole.ADMIN,
    )
    db_session.add(admin_user)
    db_session.commit()

    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@example.com", "password": "adminpass123"},
    )
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/v1/admin/users", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_normal_user_denied_admin_endpoint(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "normaluser@example.com", "password": "userpass123"},
    )
    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": "normaluser@example.com", "password": "userpass123"},
    )
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/v1/admin/users", headers=headers)
    assert response.status_code == 403
    assert response.json()["detail"] == "Operation not permitted: Insufficient permissions"


def test_user_cannot_access_other_user_note(client):
    client.post("/api/v1/auth/register", json={"email": "user1@example.com", "password": "password123"})
    login1 = client.post("/api/v1/auth/login", json={"email": "user1@example.com", "password": "password123"})
    token1 = login1.json()["access_token"]
    headers1 = {"Authorization": f"Bearer {token1}"}

    note_res = client.post("/api/v1/notes/", json={"title": "User 1 Note", "content": "Secret"}, headers=headers1)
    note_id = note_res.json()["id"]

    client.post("/api/v1/auth/register", json={"email": "user2@example.com", "password": "password123"})
    login2 = client.post("/api/v1/auth/login", json={"email": "user2@example.com", "password": "password123"})
    token2 = login2.json()["access_token"]
    headers2 = {"Authorization": f"Bearer {token2}"}

    response = client.get(f"/api/v1/notes/{note_id}", headers=headers2)
    assert response.status_code == 403
