
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db: SQLAlchemy = SQLAlchemy()
bcrypt: Bcrypt = Bcrypt()
login_manager: LoginManager = LoginManager()

__all__ = ["db", "bcrypt", "login_manager"]