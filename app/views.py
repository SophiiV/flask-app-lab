import logging
from flask import Blueprint, render_template, url_for, redirect, flash, session, request
from .forms import ContactForm

main_bp = Blueprint("main", __name__)

# простеньке логування у файл contact.log в корені проєкту
logging.basicConfig(
    filename="contact.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8",
)


@main_bp.route("/")
def index():
    return render_template("base.html", page_title="Головна", content_title="Ласкаво просимо!")


@main_bp.route("/resume")
def resume():
    return render_template("resume.html", page_title="Резюме")


@main_bp.route("/contacts", methods=["GET", "POST"])
def contacts():
    form = ContactForm()

    # даані останньої успішно відправленої форми
    contact_data = session.get("contact_data")

    if form.validate_on_submit():
        data = {
            "name": form.name.data,
            "email": form.email.data,
            "phone": form.phone.data,
            "subject": form.subject.data,
            "message": form.message.data,
        }

        # лог-файл
        logging.info(
            "Contact form submitted: name=%s, email=%s, phone=%s, subject=%s",
            data["name"],
            data["email"],
            data["phone"],
            data["subject"],
        )

        # зберегти в сесію для таблиці
        session["contact_data"] = data

        # flash з name + email
        flash(
            f"Повідомлення від {data['name']} <{data['email']}> успішно надіслано.",
            "success",
        )

        # PRG
        return redirect(url_for("main.contacts"))

    #  валідація не пройшла
    if request.method == "POST" and not form.validate():
        flash("Форма містить помилки. Перевірте введені дані.", "error")

    return render_template(
        "contacts.html",
        page_title="Контакти",
        content_title="Контакти",
        form=form,
        contact_data=contact_data,
    )
