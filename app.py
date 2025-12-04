
from __future__ import annotations

from typing import Any, Dict

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required

from config import Config
from extensions import db, bcrypt, login_manager
from forms import RegistrationForm, LoginForm
from models import User


def create_app(test_config: Dict[str, Any] | None = None) -> Flask:


    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "login"
    login_manager.login_message_category = "info"

    with app.app_context():
        db.create_all()

    @app.route("/")
    def index() -> str:

        if current_user.is_authenticated:
            return redirect(url_for("account"))
        return redirect(url_for("login"))

    @app.route("/register", methods=["GET", "POST"])
    def register() -> str:

        if current_user.is_authenticated:
            return redirect(url_for("account"))
        form = RegistrationForm()
        if form.validate_on_submit():
            # Create user and hash password
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Your account has been created! You can now log in.", "success")
            return redirect(url_for("login"))
        return render_template("register.html", form=form)

    @app.route("/login", methods=["GET", "POST"])
    def login() -> str:

        if current_user.is_authenticated:
            return redirect(url_for("account"))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get("next")
                return redirect(next_page) if next_page else redirect(url_for("account"))
            flash("Login unsuccessful. Please check email and password.", "danger")
        return render_template("login.html", form=form)

    @app.route("/logout")
    def logout() -> str:
        """Log out the current user and clear the session."""

        logout_user()
        flash("You have been logged out.", "info")
        return redirect(url_for("login"))

    @app.route("/account")
    @login_required
    def account() -> str:
        """Display the current user's profile."""

        return render_template("account.html")

    @app.route("/users")
    @login_required
    def users() -> str:
        """List all registered users for authorized users only."""

        users_list = User.query.order_by(User.username).all()
        return render_template("users.html", users=users_list)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)