from flask import Flask

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["SECRET_KEY"] = "dev-secret-key"

    # Заглушки для логіну (можеш змінити)
    app.config["LOGIN_USER"] = "sofia"
    app.config["LOGIN_PASSWORD"] = "1234"

    from .views import main_bp
    app.register_blueprint(main_bp)

    from .users.views import users_bp
    app.register_blueprint(users_bp, url_prefix="/users")

    from .products.views import products_bp
    app.register_blueprint(products_bp, url_prefix="/products")

    

    return app

app = create_app()
