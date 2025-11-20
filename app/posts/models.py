from datetime import datetime

from app import db
from sqlalchemy import String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

post_tags = db.Table(
    "post_tags",
    db.Column("post_id", db.Integer, db.ForeignKey("posts.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)


class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    posted: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    category: Mapped[str] = mapped_column(
        Enum("news", "publication", "tech", "other"),
        default="news",
        nullable=False,
    )

    author_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )
    author_obj: Mapped["User"] = relationship(
        "User",
        back_populates="posts",
    )

    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary=post_tags,
        back_populates="posts",
    )

    def __repr__(self) -> str:
        return f"<Post {self.title}>"



class Tag(db.Model):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    posts: Mapped[list[Post]] = relationship(
        "Post",
        secondary=post_tags,
        back_populates="tags",
    )

    def __repr__(self) -> str:
        return f"<Tag {self.name}>"
