from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Note
from app.forms import RegistrationForm, LoginForm


def init_routes(app):
    # Главная страница
    @app.route('/')
    def index():
        """Главная страница - список всех пользователей с количеством заметок"""
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

    # Список пользователей
    @app.route('/users')
    def show_users():
        """Простой список пользователей"""
        users = User.query.all()
        return render_template('users.html', users=users)

    # Статистика БД
    @app.route('/test-db')
    def test_db():
        """Статистика базы данных"""
        users_count = User.query.count()
        notes_count = Note.query.count()
        recent_notes = Note.query.order_by(Note.created_at.desc()).limit(3).all()

        return render_template('test_db.html',
                               users_count=users_count,
                               notes_count=notes_count,
                               recent_notes=recent_notes)

    # Заметки пользователя
    @app.route('/user/<int:user_id>/notes')
    def user_notes(user_id):
        """Показать все заметки конкретного пользователя"""
        user = User.query.get_or_404(user_id)
        notes = Note.query.filter_by(user_id=user_id).order_by(Note.created_at.desc()).all()

        return render_template('user_notes.html',
                               user=user,
                               notes=notes,
                               notes_count=len(notes))

    # Информация о тестовых данных
    @app.route('/add-test-data-info')
    def add_test_data_info():
        """Информация о добавлении тестовых данных"""
        return render_template('add_test_info.html')

    # Регистрация
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(username=form.username.data,
                        email=form.email.data)
            user.set_password(form.password.data)

            db.session.add(user)
            db.session.commit()

            flash('Регистрация успешна! Теперь вы можете войти.', 'success')
            return redirect(url_for('login'))

        return render_template('register.html', form=form)

    # Вход
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()

            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Вы успешно вошли!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Неверное имя пользователя или пароль', 'danger')

        return render_template('login.html', form=form)

    # Выход
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Вы вышли из системы', 'info')
        return redirect(url_for('index'))

    # Профиль
    @app.route('/profile')
    @login_required
    def profile():
        return f"Привет, {current_user.username}! Это ваш профиль."