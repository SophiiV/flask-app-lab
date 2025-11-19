import os

from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .config import config_map


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name: str | None = None) -> Flask:
    """Application factory that creates and configures the Flask app instance."""
    app = Flask(__name__, instance_relative_config=True)

    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG", "development")

    app.config.from_object(config_map[config_name])


    db.init_app(app)
    migrate.init_app(app, db)


    from .posts import bp as posts_bp

    app.register_blueprint(posts_bp)


    @app.route("/")
    def index():
        return redirect(url_for("posts.list_posts"))


    @app.errorhandler(404)
    def page_not_found(error):  # noqa: ARG001
        return render_template("404.html"), 404

    return app
