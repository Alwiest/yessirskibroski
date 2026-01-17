# add_test_data.py
from app import create_app
from app.models import db, User, Note
from datetime import datetime

app = create_app()

with app.app_context():
    print("🔄 Очищаем старые данные...")

    # Очищаем таблицы
    Note.query.delete()
    User.query.delete()
    db.session.commit()

    print("👥 Создаем пользователей...")

    # Обычные пользователи
    user1 = User(username="alex", email="alex@mail.com", is_admin=False)
    user1.set_password("123")  # используем метод set_password

    user2 = User(username="masha", email="masha@mail.com", is_admin=False)
    user2.set_password("456")

    user3 = User(username="ivan", email="ivan@mail.com", is_admin=False)
    user3.set_password("789")

    # Администратор
    admin = User(username="admin", email="admin@example.com", is_admin=True)
    admin.set_password("admin123")

    db.session.add_all([user1, user2, user3, admin])
    db.session.commit()

    print("📝 Создаем заметки...")
    notes = [
        Note(
            title="Список покупок",
            content="Молоко, хлеб, яйца, масло, сыр",
            tags="еда,дом,покупки",
            user_id=1,
            created_at=datetime(2024, 1, 15, 10, 30),
            updated_at=datetime(2024, 1, 15, 10, 30)
        ),
        Note(
            title="Рабочие задачи на неделю",
            content="1. Завершить проект Flask\n2. Написать тесты\n3. Обновить документацию",
            tags="работа,срочно,проект",
            user_id=1,
            created_at=datetime(2024, 1, 14, 9, 15),
            updated_at=datetime(2024, 1, 16, 14, 20)
        ),
        Note(
            title="Книги для саморазвития",
            content="• Чистый код - Роберт Мартин\n• Паттерны проектирования\n• Алгоритмы на Python",
            tags="развитие,книги,программирование",
            user_id=2,
            created_at=datetime(2024, 1, 10, 16, 45),
            updated_at=datetime(2024, 1, 12, 11, 30)
        ),
        Note(
            title="План тренировок в зале",
            content="ПН: Грудь, трицепс\nСР: Спина, бицепс\nПТ: Ноги, плечи\nВС: Кардио",
            tags="спорт,здоровье,тренировки",
            user_id=3,
            created_at=datetime(2024, 1, 5, 8, 0),
            updated_at=datetime(2024, 1, 15, 18, 45)
        ),
        Note(
            title="Административные задачи системы",
            content="1. Мониторинг работы сервера\n2. Добавление новых пользователей\n3. Проверка безопасности\n4. Резервное копирование",
            tags="админ,работа,управление",
            user_id=4,
            created_at=datetime(2024, 1, 1, 12, 0),
            updated_at=datetime(2024, 1, 16, 9, 30)
        ),
    ]

    for note in notes:
        db.session.add(note)
    db.session.commit()

    print("\n" + "=" * 50)
    print("✅ ТЕСТОВЫЕ ДАННЫЕ УСПЕШНО СОЗДАНЫ")
    print("=" * 50)
    print(f"👥 Пользователей: {User.query.count()}")
    print(f"👑 Админов: {User.query.filter_by(is_admin=True).count()}")
    print(f"📝 Заметок: {Note.query.count()}")
    print("\n🔑 ДАННЫЕ ДЛЯ ВХОДА:")
    print("   Обычный пользователь: alex / 123")
    print("   Администратор: admin / admin123")
    print("\n📊 СТАТИСТИКА ПОЛЬЗОВАТЕЛЕЙ:")

    users = User.query.all()
    for user in users:
        notes_count = Note.query.filter_by(user_id=user.id).count()
        role = "👑 АДМИН" if user.is_admin else "👤 ПОЛЬЗОВАТЕЛЬ"
        print(f"   {role}: {user.username} ({user.email}) - {notes_count} заметок")

    print("=" * 50)
    print("\n🚀 Запустите сервер: python run.py")
    print("🌐 Откройте в браузере: http://localhost:5000")