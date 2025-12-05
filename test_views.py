
from flask import url_for


def test_register_page_loads(client) -> None:

    response = client.get("/register")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Register" in html


def test_login_page_loads(client) -> None:

    response = client.get("/login")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Login" in html