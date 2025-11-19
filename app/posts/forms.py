from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    BooleanField,
    DateTimeLocalField,
    SelectField,
    SubmitField,
)
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    """Form for creating and editing posts."""

    title = StringField(
        "Title",
        validators=[DataRequired(), Length(min=3, max=150)],
    )
    content = TextAreaField(
        "Content",
        validators=[DataRequired(), Length(min=10)],
    )
    enabled = BooleanField("Active", default=True)
    publish_date = DateTimeLocalField(
        "Publish at",
        format="%Y-%m-%dT%H:%M",
        default=datetime.utcnow,
    )
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
    submit = SubmitField("Save")
