from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-key-123-change-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Настройки Flask-Login
    login_manager.login_view = 'login'  # куда перенаправлять неавторизованных
    login_manager.login_message = 'Пожалуйста, войдите чтобы получить доступ к этой странице'
    login_manager.login_message_category = 'warning'

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app import routes
    routes.init_routes(app)

    return app