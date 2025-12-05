

def test_account_requires_login(client) -> None:

    response = client.get("/account", follow_redirects=True)
    html = response.get_data(as_text=True)
    assert "Login" in html


def test_users_requires_login(client) -> None:

    response = client.get("/users", follow_redirects=True)
    html = response.get_data(as_text=True)
    assert "Login" in html