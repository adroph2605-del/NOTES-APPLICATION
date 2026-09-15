def get_auth_headers(client, email="noteuser@example.com"):
    client.post("/api/v1/auth/register", json={"email": email, "password": "password123"})
    login_res = client.post("/api/v1/auth/login", json={"email": email, "password": "password123"})
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_and_read_note(client):
    headers = get_auth_headers(client)

    create_res = client.post(
        "/api/v1/notes/",
        json={"title": "Test Title", "content": "Test Content"},
        headers=headers,
    )
    assert create_res.status_code == 201
    note_id = create_res.json()["id"]

    read_res = client.get(f"/api/v1/notes/{note_id}", headers=headers)
    assert read_res.status_code == 200
    assert read_res.json()["title"] == "Test Title"
