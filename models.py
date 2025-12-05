
from __future__ import annotations

from datetime import datetime

from flask_login import UserMixin

from extensions import db, bcrypt, login_manager


class User(db.Model, UserMixin):

    __tablename__ = "users"

    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(64), unique=True, nullable=False)
    email: str = db.Column(db.String(120), unique=True, nullable=False)
    password_hash: str = db.Column(db.String(128), nullable=False)

    image: str = db.Column(
        db.String(120), nullable=True, default="profile_default.jpg"
    )
    about_me: str | None = db.Column(db.Text, nullable=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<User {self.username}>"

    def set_password(self, password: str) -> None:

        self.password_hash = bcrypt.generate_password_hash(password).decode(
            "utf-8"
        )

    def check_password(self, password: str) -> bool:

        return bcrypt.check_password_hash(self.password_hash, password)


@login_manager.user_loader  # type: ignore[misc]
def load_user(user_id: str) -> User | None:
   
    try:
        return User.query.get(int(user_id))  # type: ignore[call-arg]
    except (ValueError, TypeError):
        return None