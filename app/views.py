from flask import Blueprint, render_template, url_for, redirect, flash, session
from .forms import ContactForm

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("base.html", page_title="Головна", content_title="Ласкаво просимо!")


@main_bp.route("/resume")
def resume():
    return render_template("resume.html", page_title="Резюме")


@main_bp.route("/contacts", methods=["GET", "POST"])
def contacts():
    form = ContactForm()

    # Дані останньої відправленої форми (для таблиці)
    contact_data = session.get("contact_data")

    if form.validate_on_submit():
        # Зберігаємо дані в сесію (для відображення у вигляді таблиці після redirect)
        session["contact_data"] = {
            "name": form.name.data,
            "email": form.email.data,
            "message": form.message.data,
            "agree": form.agree.data,
        }

        flash("Повідомлення успішно відправлено.", "success")
        # Post/Redirect/Get
        return redirect(url_for("main.contacts"))

    return render_template(
        "contacts.html",
        page_title="Контакти",
        content_title="Контакти",
        form=form,
        contact_data=contact_data,
    )
