# add_test_data.py
from app import create_app
from app.models import db, User, Note
from datetime import datetime

app = create_app()

with app.app_context():
    print("🔄 Очищаем старые данные...")
    db.drop_all()
    db.create_all()

    print("👥 Создаем пользователей...")
    # Используем set_password для хеширования
    user1 = User(username="alex", email="alex@mail.com")
    user1.set_password("123")

    user2 = User(username="masha", email="masha@mail.com")
    user2.set_password("456")

    user3 = User(username="ivan", email="ivan@mail.com")
    user3.set_password("789")

    db.session.add_all([user1, user2, user3])
    db.session.commit()

    print("📝 Создаем заметки...")
    notes = [
        Note(title="Покупки", content="Молоко, хлеб, яйца", tags="еда,дом", user_id=1),
        Note(title="Работа", content="Сделать проект по Flask", tags="работа,срочно", user_id=1),
        Note(title="Книги", content="Прочитать 'Чистый код'", tags="развитие,книги", user_id=2),
        Note(title="Спорт", content="Сходить в зал", tags="здоровье", user_id=3),
    ]

    for note in notes:
        db.session.add(note)
    db.session.commit()

    print(f"✅ Готово! Пользователей: {User.query.count()}, Заметок: {Note.query.count()}")