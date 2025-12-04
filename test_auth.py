

from __future__ import annotations

from typing import Any

from extensions import db
from models import User


def register(client, username: str, email: str, password: str) -> Any:

    return client.post(
        "/register",
        data={
            "username": username,
            "email": email,
            "password": password,
            "confirm_password": password,
            "submit": True,
        },
        follow_redirects=True,
    )


def login(client, email: str, password: str, remember: bool = False) -> Any:
    """Helper function to log in a user."""

    return client.post(
        "/login",
        data={
            "email": email,
            "password": password,
            "remember": remember,
            "submit": True,
        },
        follow_redirects=True,
    )


def test_user_registration_saves_user(client, app) -> None:

    response = register(client, "newuser", "new@example.com", "secret123")
    assert response.status_code == 200
    # Verify user exists in DB
    with app.app_context():
        user = User.query.filter_by(username="newuser").first()
        assert user is not None
        assert user.email == "new@example.com"


def test_login_and_logout(client, app) -> None:
    """Test the full login and logout flow."""

    register(client, "loginuser", "login@example.com", "password123")
    response = login(client, "login@example.com", "password123")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Account" in html or "Your Profile" in html

    with client.session_transaction() as sess:
        assert "_user_id" in sess

    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    with client.session_transaction() as sess:
        assert "_user_id" not in sess