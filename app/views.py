from flask import Blueprint, render_template, url_for

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return render_template("base.html", page_title="Головна", content_title="Ласкаво просимо!")

@main_bp.route("/resume")
def resume():
    return render_template("resume.html", page_title="Резюме")

@main_bp.route("/contacts")
def contacts():
    return render_template("base.html", page_title="Контакти", content_title="Контакти")
