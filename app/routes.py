from flask import render_template
from app import db
from app.models import User, Note


def init_routes(app):
    @app.route('/')
    def index():
        # Временная заглушка
        return "Приложение работает! <a href='/users'>Перейти к пользователям</a>"

    @app.route('/users')
    def users():
        # Просто показываем, что есть в базе
        users = User.query.all()
        return f"Пользователей в базе: {len(users)}"