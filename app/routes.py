from flask import render_template
from app.models import User, Note


def init_routes(app):
    @app.route('/')
    def index():
        """Главная страница - список всех пользователей"""
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

    @app.route('/users')
    def show_users():
        """Простой список пользователей - используем шаблон"""
        users = User.query.all()
        return render_template('users.html', users=users)

    @app.route('/test-db')
    def test_db():
        """Статистика БД - используем шаблон"""
        users_count = User.query.count()
        notes_count = Note.query.count()
        recent_notes = Note.query.order_by(Note.created_at.desc()).limit(3).all()

        return render_template('test_db.html',
                               users_count=users_count,
                               notes_count=notes_count,
                               recent_notes=recent_notes)

    @app.route('/add-test-data-info')
    def add_test_data_info():
        """Информация о добавлении тестовых данных"""
        return render_template('add_test_info.html')

    @app.route('/user/<int:user_id>/notes')
    def user_notes(user_id):
        """Показать все заметки конкретного пользователя"""
        user = User.query.get_or_404(user_id)
        notes = Note.query.filter_by(user_id=user_id).order_by(Note.created_at.desc()).all()

        return render_template('user_notes.html',
                               user=user,
                               notes=notes,
                               notes_count=len(notes))