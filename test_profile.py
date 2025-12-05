

from models import User


def register(client, username: str, email: str, password: str):
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


def login(client, email: str, password: str):
    return client.post(
        "/login",
        data={
            "email": email,
            "password": password,
            "submit": True,
        },
        follow_redirects=True,
    )


def test_update_account_changes_data(client, app):

    register(client, "profuser", "prof@example.com", "pass1234")
    login(client, "prof@example.com", "pass1234")
    # Update profile
    response = client.post(
        "/account",
        data={
            "username": "professor",
            "email": "prof2@example.com",
            "about_me": "About me updated",
            # no picture uploaded in test
            "submit": True,
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Your account has been updated" in response.get_data(as_text=True)
    with app.app_context():
        user = User.query.filter_by(email="prof2@example.com").first()
        assert user is not None
        assert user.username == "professor"
        assert user.about_me == "About me updated"


def test_change_password(client, app):

    register(client, "changepw", "changepw@example.com", "oldpass1")
    login(client, "changepw@example.com", "oldpass1")
    resp = client.post(
        "/change_password",
        data={
            "old_password": "wrongpass",
            "new_password": "newpass1",
            "confirm_password": "newpass1",
            "submit": True,
        },
        follow_redirects=True,
    )
    assert "Incorrect current password" in resp.get_data(as_text=True)
    resp = client.post(
        "/change_password",
        data={
            "old_password": "oldpass1",
            "new_password": "newpass1",
            "confirm_password": "newpass1",
            "submit": True,
        },
        follow_redirects=True,
    )
    assert "Your password has been updated" in resp.get_data(as_text=True)
    client.get("/logout", follow_redirects=True)
    resp = login(client, "changepw@example.com", "newpass1")
    assert resp.status_code == 200
    assert "Your Profile" in resp.get_data(as_text=True)