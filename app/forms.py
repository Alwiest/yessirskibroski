from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя',
                           validators=[DataRequired(),
                                       Length(min=3, max=80)])
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email()])
    password = PasswordField('Пароль',
                             validators=[DataRequired(),
                                         Length(min=6)])
    confirm_password = PasswordField('Подтвердите пароль',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя пользователя уже занято.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Этот email уже зарегистрирован.')


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя',
                           validators=[DataRequired()])
    password = PasswordField('Пароль',
                             validators=[DataRequired()])
    submit = SubmitField('Войти')


class NoteForm(FlaskForm):
    title = StringField('Заголовок', validators=[
        DataRequired(message='Заголовок обязателен'),
        Length(max=100, message='Максимум 100 символов')
    ])
    content = TextAreaField('Текст заметки', validators=[
        DataRequired(message='Текст заметки обязателен')
    ])
    tags = StringField('Теги (через запятую)', validators=[
        Length(max=200, message='Максимум 200 символов')
    ])
    submit = SubmitField('Сохранить')