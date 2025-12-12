from flask import render_template
from app import db
from app.models import User, Note


def init_routes(app):
    @app.route('/')
    def index():
        # Получаем всех пользователей и количество их заметок
        users = User.query.all()
        user_stats = []

        for user in users:
            notes_count = Note.query.filter_by(user_id=user.id).count()
            user_stats.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'notes_count': notes_count
            })

        return render_template('index.html', users=user_stats)