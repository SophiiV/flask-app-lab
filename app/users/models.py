from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    # 1:N – один користувач має багато постів
    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="author_obj",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<User {self.username}>"
