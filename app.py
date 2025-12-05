
from __future__ import annotations

from typing import Any, Dict

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required

from config import Config
from extensions import db, bcrypt, login_manager
from forms import RegistrationForm, LoginForm, UpdateAccountForm, ChangePasswordForm
from models import User

import os
import secrets
from datetime import datetime
from PIL import Image


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


    @app.before_request
    def before_request_func() -> None:
        if current_user.is_authenticated:
            current_user.last_seen = datetime.utcnow()
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()

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

        logout_user()
        flash("You have been logged out.", "info")
        return redirect(url_for("login"))

    @app.route("/account", methods=["GET", "POST"])
    @login_required
    def account() -> str:

        form = UpdateAccountForm()
        form._current_user = current_user  # type: ignore[attr-defined]
        if request.method == "GET":
            form.username.data = current_user.username
            form.email.data = current_user.email
            form.about_me.data = current_user.about_me
        if form.validate_on_submit():
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.about_me = form.about_me.data
            if form.picture.data:
                picture_file, thumb_file = save_picture(form.picture.data)
                current_user.image = picture_file
            db.session.commit()
            flash("Your account has been updated.", "success")
            return redirect(url_for("account"))
        return render_template("account.html", form=form)

    @app.route("/users")
    @login_required
    def users() -> str:

        users_list = User.query.order_by(User.username).all()
        return render_template("users.html", users=users_list)

    @app.route("/change_password", methods=["GET", "POST"])
    @login_required
    def change_password() -> str:

        form = ChangePasswordForm()
        if form.validate_on_submit():
            if not current_user.check_password(form.old_password.data):
                flash("Incorrect current password.", "danger")
            else:
                current_user.set_password(form.new_password.data)
                db.session.commit()
                flash("Your password has been updated.", "success")
                return redirect(url_for("account"))
        return render_template("change_password.html", form=form)

    def save_picture(form_picture):

        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        thumb_fn = random_hex + "_thumb" + f_ext
        picture_path = os.path.join(app.static_folder, "profile_pics", picture_fn)
        thumb_path = os.path.join(app.static_folder, "profile_pics", thumb_fn)
        os.makedirs(os.path.dirname(picture_path), exist_ok=True)
        form_picture.save(picture_path)
        try:
            img = Image.open(picture_path)
            img.thumbnail((128, 128))
            img.save(thumb_path)
        except Exception:
            import shutil

            shutil.copy(picture_path, thumb_path)
        return picture_fn, thumb_fn

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)