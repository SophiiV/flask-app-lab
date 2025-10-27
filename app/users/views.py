from flask import Blueprint, render_template, request, redirect, url_for

users_bp = Blueprint(
    "users",
    __name__,
    template_folder="templates",
)

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
    # редірект як у прикладі з методички:
    # /hi/ADMINISTRATOR?age=19
    return redirect(url_for("users.greetings", name="ADMINISTRATOR", age=19))
