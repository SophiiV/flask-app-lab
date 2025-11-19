from datetime import datetime

from sqlalchemy import String, Text, DateTime, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app import db


class Post(db.Model):
    """ORM model representing a blog post."""

    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    posted: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    category: Mapped[str] = mapped_column(
        Enum("news", "publication", "tech", "other", name="post_category"),
        default="other",
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    author: Mapped[str] = mapped_column(
        String(20),
        default="Anonymous",
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Post {self.id} {self.title!r}>"
