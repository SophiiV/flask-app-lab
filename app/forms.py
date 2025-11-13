from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    BooleanField,
    PasswordField,
    SubmitField,
    SelectField,
)
from wtforms.validators import DataRequired, Email, Length, Regexp


class ContactForm(FlaskForm):
    name = StringField(
        "Ім’я",
        validators=[
            DataRequired(message="Вкажіть ім’я."),
            Length(min=4, max=10, message="Ім’я має бути від 4 до 10 символів."),
        ],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Вкажіть email."),
            Email(message="Некоректний формат email."),
        ],
    )
    phone = StringField(
        "Телефон",
        validators=[
            DataRequired(message="Вкажіть номер телефону."),
            Regexp(
                r"^\+380\d{9}$",
                message="Формат телефону має бути: +380XXXXXXXXX (9 цифр після коду).",
            ),
        ],
    )
    subject = SelectField(
        "Тема",
        choices=[
            ("support", "Підтримка"),
            ("order", "Питання щодо замовлення"),
            ("feedback", "Відгук"),
            ("other", "Інше"),
        ],
        validators=[DataRequired(message="Оберіть тему звернення.")],
    )
    message = TextAreaField(
        "Повідомлення",
        validators=[
            DataRequired(message="Вкажіть текст повідомлення."),
            Length(
                max=500,
                message="Повідомлення не повинно перевищувати 500 символів.",
            ),
        ],
    )
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
