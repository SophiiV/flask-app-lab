
from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from extensions import db
from models import User


class RegistrationForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=4, max=25, message="Username must be between 4 and 25 characters"),
        ],
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6, message="Password must be at least 6 characters")],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match")],
    )
    submit = SubmitField("Register")

    def validate_username(self, field: StringField) -> None:
        """Ensure the username is unique."""

        if User.query.filter_by(username=field.data).first():
            raise ValidationError("This username is already taken")

    def validate_email(self, field: StringField) -> None:
        """Ensure the email is unique."""

        if User.query.filter_by(email=field.data).first():
            raise ValidationError("This email is already registered")


class LoginForm(FlaskForm):
    """Form for logging in an existing user."""

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
    )
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")