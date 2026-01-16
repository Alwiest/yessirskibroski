from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Note
from app.forms import RegistrationForm, LoginForm, NoteForm


def init_routes(app):
    @app.route('/')
    def index():
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
        users = User.query.all()
        return render_template('users.html', users=users)

    @app.route('/test-db')
    def test_db():
        users_count = User.query.count()
        notes_count = Note.query.count()
        recent_notes = Note.query.order_by(Note.created_at.desc()).limit(3).all()
        return render_template('test_db.html',
                               users_count=users_count,
                               notes_count=notes_count,
                               recent_notes=recent_notes)

    @app.route('/user/<int:user_id>/notes')
    def user_notes(user_id):
        user = User.query.get_or_404(user_id)
        notes = Note.query.filter_by(user_id=user_id).order_by(Note.created_at.desc()).all()
        return render_template('user_notes.html',
                               user=user,
                               notes=notes,
                               notes_count=len(notes))

    @app.route('/add-test-data-info')
    def add_test_data_info():
        return render_template('add_test_info.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Регистрация успешна!', 'success')
            return redirect(url_for('login'))
        return render_template('register.html', form=form)

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

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Вы вышли из системы', 'info')
        return redirect(url_for('index'))

    @app.route('/profile')
    @login_required
    def profile():
        notes_count = Note.query.filter_by(user_id=current_user.id).count()
        return render_template('profile.html', user=current_user, notes_count=notes_count)

    @app.route('/notes')
    @login_required
    def notes_list():
        notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.created_at.desc()).all()
        return render_template('notes/list.html', notes=notes)

    @app.route('/notes/new', methods=['GET', 'POST'])
    @login_required
    def new_note():
        form = NoteForm()
        if form.validate_on_submit():
            note = Note(
                title=form.title.data,
                content=form.content.data,
                tags=form.tags.data,
                user_id=current_user.id
            )
            db.session.add(note)
            db.session.commit()
            flash('Заметка создана!', 'success')
            return redirect(url_for('notes_list'))
        return render_template('notes/new.html', form=form)

    @app.route('/notes/<int:note_id>')
    @login_required
    def view_note(note_id):
        note = Note.query.get_or_404(note_id)
        if note.user_id != current_user.id:
            flash('Нет доступа к заметке', 'danger')
            return redirect(url_for('notes_list'))
        return render_template('notes/view.html', note=note)

    @app.route('/notes/<int:note_id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_note(note_id):
        note = Note.query.get_or_404(note_id)
        if note.user_id != current_user.id:
            flash('Нет доступа к заметке', 'danger')
            return redirect(url_for('notes_list'))
        form = NoteForm(obj=note)
        if form.validate_on_submit():
            note.title = form.title.data
            note.content = form.content.data
            note.tags = form.tags.data
            db.session.commit()
            flash('Заметка обновлена!', 'success')
            return redirect(url_for('view_note', note_id=note.id))
        return render_template('notes/edit.html', form=form, note=note)

    @app.route('/notes/<int:note_id>/delete', methods=['POST'])
    @login_required
    def delete_note(note_id):
        note = Note.query.get_or_404(note_id)
        if note.user_id != current_user.id:
            flash('Нет доступа к заметке', 'danger')
            return redirect(url_for('notes_list'))
        db.session.delete(note)
        db.session.commit()
        flash('Заметка удалена!', 'success')
        return redirect(url_for('notes_list'))

    @app.route('/notes/search')
    @login_required
    def search_notes():
        query = request.args.get('q', '')
        if query:
            notes = Note.query.filter(
                Note.user_id == current_user.id,
                (Note.title.contains(query)) |
                (Note.content.contains(query)) |
                (Note.tags.contains(query))
            ).order_by(Note.created_at.desc()).all()
        else:
            notes = []
        return render_template('notes/search.html', notes=notes, query=query, notes_count=len(notes))
