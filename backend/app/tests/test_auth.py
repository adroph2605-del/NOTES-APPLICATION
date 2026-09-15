def test_register_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "testuser@example.com", "password": "password123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert "id" in data


def test_login_user(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "loginuser@example.com", "password": "password123"},
    )

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "loginuser@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_register_user_with_stale_sqlite_schema():
    import sqlite3
    from pathlib import Path

    from app.core.database import ensure_database_schema

    db_path = Path("./test_stale_schema.db")
    if db_path.exists():
        db_path.unlink()

    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                email TEXT UNIQUE,
                hashed_password TEXT,
                role TEXT
            )
            """
        )
        conn.commit()

    try:
        ensure_database_schema(f"sqlite:///{db_path}")

        with sqlite3.connect(db_path) as conn:
            columns = [row[1] for row in conn.execute("PRAGMA table_info(users)").fetchall()]
        assert "is_active" in columns
    finally:
        if db_path.exists():
            try:
                db_path.unlink()
            except PermissionError:
                pass
