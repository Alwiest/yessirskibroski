from app import create_app
from app.models import db, User, Note
from datetime import datetime

app = create_app()

with app.app_context():
    # Очищаем старые данные
    db.drop_all()
    db.create_all()

    # Создаем пользователей
    users = [
        User(username="denchik", email="duralei@example.com", password="123"),
        User(username="siniy", email="siniy@example.com", password="456"),
        User(username="vyach", email="vyach@example.com", password="789"),
    ]

    for user in users:
        db.session.add(user)
    db.session.commit()

    # Создаем заметки
    notes = [
        Note(title="Список покупок", content="Молоко, хлеб, яйца",
             tags="покупки,дом", user_id=1),
        Note(title="Учеба", content="Сделать проект по Flask",
             tags="работа,срочно", user_id=1),
        Note(title="Книги", content="Прочитать 'Чистый код'",
             tags="развитие", user_id=2),
        Note(title="Спорт", content="Сходить в зал",
             tags="здоровье", user_id=3),
    ]

    for note in notes:
        db.session.add(note)
    db.session.commit()

    print(f"✅ Создано: {User.query.count()} пользователей")
    print(f"✅ Создано: {Note.query.count()} заметок")