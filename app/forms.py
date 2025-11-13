from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    name = StringField(
        "Ім’я",
        validators=[
            DataRequired(message="Вкажіть ім’я."),
            Length(max=50, message="Ім’я занадто довге."),
        ],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Вкажіть email."),
            Email(message="Некоректний формат email."),
            Length(max=120),
        ],
    )
    message = TextAreaField(
        "Повідомлення",
        validators=[
            DataRequired(message="Вкажіть текст повідомлення."),
            Length(min=10, max=1000, message="Повідомлення має бути від 10 до 1000 символів."),
        ],
    )
    agree = BooleanField("Я погоджуюсь з обробкою персональних даних")
    submit = SubmitField("Відправити")


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(message="Введіть ім’я користувача.")],
    )
    password = PasswordField(
        "Пароль",
        validators=[DataRequired(message="Введіть пароль.")],
    )
    remember = BooleanField("Запам’ятати мене")
    submit = SubmitField("Увійти")
