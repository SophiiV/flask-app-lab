from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    SelectField,
    SelectMultipleField,
)
from wtforms.validators import DataRequired

from app.users.models import User
from app.posts.models import Tag


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])

    category = SelectField(
        "Category",
        choices=[
            ("news", "News"),
            ("publication", "Publication"),
            ("tech", "Tech"),
            ("other", "Other"),
        ],
        validators=[DataRequired()],
    )

    author_id = SelectField("Author", coerce=int)

    tags = SelectMultipleField("Tags", coerce=int)

    submit = SubmitField("Save")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # автори з БД
        self.author_id.choices = [
            (u.id, u.username) for u in User.query.order_by(User.id)
        ]

        # теги з БД
        self.tags.choices = [(t.id, t.name) for t in Tag.query.order_by(Tag.name)]
