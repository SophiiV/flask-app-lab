from datetime import timedelta

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    make_response,
    current_app,
)

from ..forms import LoginForm

users_bp = Blueprint("users", __name__, template_folder="templates")


@users_bp.route("/hi/<name>")
def greetings(name):
    age = request.args.get("age", type=int)
    return render_template(
        "users/hi.html",
            page_title="Hi",
            content_title="Users / Hi",
            name=name,
            age=age,
    )


@users_bp.route("/admin")
def admin():
    return redirect(url_for("users.greetings", name="ADMINISTRATOR", age=19))


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data.strip().lower()
        password = form.password.data.strip()

        if (
            username == current_app.config["LOGIN_USER"]
            and password == current_app.config["LOGIN_PASSWORD"]
        ):
            session["user"] = username

            # remember → робимо сесію "постійною"
            session.permanent = form.remember.data
            if form.remember.data:
                flash(
                    "Вхід успішний. Ви будете запам’ятані на цьому пристрої.",
                    "success",
                )
            else:
                flash(
                    "Вхід успішний. Сесія діятиме до закриття браузера.",
                    "success",
                )

            # Post/Redirect/Get
            return redirect(url_for("users.profile"))

        # Невірні дані → flash + redirect назад на /login
        flash("Невірний логін або пароль.", "error")
        return redirect(url_for("users.login"))

    # GET-запит або перший показ форми
    return render_template(
        "users/login.html",
        page_title="Вхід",
        content_title="Login",
        form=form,
    )


@users_bp.route("/profile")
def profile():
    if "user" not in session:
        flash("Увійдіть у систему, щоб переглянути профіль.", "error")
        return redirect(url_for("users.login"))

    theme = request.cookies.get("theme", "light")
    return render_template(
        "users/profile.html",
        page_title="Профіль",
        content_title="Профіль користувача",
        theme=theme,
        cookies=request.cookies.items(),
    )


@users_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    flash("Ви вийшли із системи.", "success")
    return redirect(url_for("users.login"))


@users_bp.route("/cookie/add", methods=["POST"])
def add_cookie():
    if "user" not in session:
        flash("Спочатку увійдіть.", "error")
        return redirect(url_for("users.login"))

    key = request.form.get("key", "").strip()
    value = request.form.get("value", "").strip()
    ttl = request.form.get("ttl", type=int) or 60  # хвилин

    if not key:
        flash("Ключ кукі не може бути порожнім.", "error")
        return redirect(url_for("users.profile"))

    resp = make_response(redirect(url_for("users.profile")))
    resp.set_cookie(key, value, max_age=ttl * 60)
    flash(f"Кукі '{key}' додано на {ttl} хв.", "success")
    return resp


@users_bp.route("/cookie/delete", methods=["POST"])
def delete_cookie():
    if "user" not in session:
        flash("Спочатку увійдіть.", "error")
        return redirect(url_for("users.login"))

    key = request.form.get("key", "").strip()
    resp = make_response(redirect(url_for("users.profile")))
    if key:
        resp.delete_cookie(key)
        flash(f"Кукі '{key}' видалено.", "success")
    else:
        # видалити всі
        for k in request.cookies.keys():
            resp.delete_cookie(k)
        flash("Всі кукі видалено.", "success")
    return resp


@users_bp.route("/theme/<mode>")
def set_theme(mode: str):
    if "user" not in session:
        flash("Спочатку увійдіть.", "error")
        return redirect(url_for("users.login"))

    mode = mode.lower()
    if mode not in ("light", "dark"):
        flash("Невідома тема. Доступні: light, dark.", "error")
        return redirect(url_for("users.profile"))

    resp = make_response(redirect(url_for("users.profile")))
    # 90 днів
    resp.set_cookie("theme", mode, max_age=int(timedelta(days=90).total_seconds()))
    flash(f"Тему змінено на {mode}.", "success")
    return resp
