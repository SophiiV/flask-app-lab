
from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
)
from flask_wtf.file import FileField, FileAllowed

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


class UpdateAccountForm(FlaskForm):

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
    about_me = TextAreaField(
        "About me",
        validators=[Length(max=500, message="About me must be less than 500 characters")],
    )
    picture = FileField(
        "Update Profile Picture",
        validators=[FileAllowed(["jpg", "png", "jpeg"], "Images only!")],
    )
    submit = SubmitField("Update")

    def validate_username(self, field: StringField) -> None:
        user = User.query.filter_by(username=field.data).first()

        if user and hasattr(self, "_current_user") and user != self._current_user:
            raise ValidationError("This username is already taken")

    def validate_email(self, field: StringField) -> None:
        """Validate that the new email is either unchanged or unique."""

        user = User.query.filter_by(email=field.data).first()
        if user and hasattr(self, "_current_user") and user != self._current_user:
            raise ValidationError("This email is already registered")


class ChangePasswordForm(FlaskForm):

    old_password = PasswordField("Current Password", validators=[DataRequired()])
    new_password = PasswordField(
        "New Password",
        validators=[DataRequired(), Length(min=6, message="Password must be at least 6 characters")],
    )
    confirm_password = PasswordField(
        "Confirm New Password",
        validators=[DataRequired(), EqualTo("new_password", message="Passwords must match")],
    )
    submit = SubmitField("Change Password")