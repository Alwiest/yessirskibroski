# setup_project.py - ИСПРАВЛЕННАЯ ВЕРСИЯ
import os
import sys
import subprocess
import sqlite3
from datetime import datetime

print("=" * 60)
print("🚀 УСТАНОВКА ПРОЕКТА NOTES APP (ИСПРАВЛЕННАЯ)")
print("=" * 60)


def run_command(cmd, description):
    print(f"\n📌 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ Успешно")
            if result.stdout.strip():
                print(f"   📝 {result.stdout.strip()}")
        else:
            print(f"   ❌ Ошибка: {result.stderr.strip()}")
            return False
        return True
    except Exception as e:
        print(f"   ❌ Исключение: {e}")
        return False


def main():
    # 1. Проверка Python
    print("\n🔍 Проверка окружения...")
    print(f"   Python версия: {sys.version}")

    # 2. Установка зависимостей
    print("\n📦 Установка зависимостей...")
    dependencies = [
        "Flask==2.3.3",
        "Flask-SQLAlchemy==3.0.5",
        "Flask-Migrate==4.0.4",
        "Flask-Login==0.6.2",
        "Flask-WTF==1.2.1",
        "Werkzeug==2.3.0"
    ]

    for dep in dependencies:
        run_command(f"pip install {dep}", f"Установка {dep}")

    # 3. Создание структуры папок
    print("\n📁 Создание структуры папок...")
    folders = ['instance', 'templates', 'templates/notes', 'templates/auth', 'migrations']
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"   ✅ Создана папка: {folder}")

    # 4. СОЗДАНИЕ БАЗЫ ДАННЫХ С ПРАВИЛЬНОЙ СТРУКТУРОЙ
    print("\n🗄️  Создание базы данных...")

    db_path = 'app/instance/notes.db'
    if os.path.exists(db_path):
        os.remove(db_path)
        print("   🔄 Удалена старая база данных")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # ТАБЛИЦА user - ТОЧНО КАК В models.py (password, НЕ password_hash!)
    cursor.execute('''
    CREATE TABLE user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(80) UNIQUE NOT NULL,
        email VARCHAR(120) UNIQUE NOT NULL,
        password VARCHAR(200) NOT NULL,  -- ← ИМЕННО password
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    print("   ✅ Таблица 'user' создана")

    # ТАБЛИЦА note - ТОЧНО КАК В models.py
    cursor.execute('''
    CREATE TABLE note (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(100) NOT NULL,
        content TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        tags VARCHAR(200),
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES user (id)
    )
    ''')
    print("   ✅ Таблица 'note' создана")

    conn.commit()

    # 5. Проверка структуры
    print("\n🔍 Проверка структуры базы данных...")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"   📊 Таблиц в базе: {len(tables)}")

    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        print(f"\n   📋 Таблица '{table_name}':")
        for col in columns:
            print(f"      - {col[1]}: {col[2]} {'(PK)' if col[5] else ''}")

    # 6. СОЗДАНИЕ ТЕСТОВЫХ ДАННЫХ
    print("\n👥 Добавление тестовых данных...")

    # Тестовые пользователи (пароли как есть)
    test_users = [
        ("alex", "alex@mail.com", "123"),
        ("masha", "masha@mail.com", "456"),
        ("ivan", "ivan@mail.com", "789")
    ]

    for username, email, password in test_users:
        cursor.execute(
            "INSERT INTO user (username, email, password) VALUES (?, ?, ?)",
            (username, email, password)
        )
        print(f"   👤 Создан пользователь: {username}")

    # Тестовые заметки
    test_notes = [
        ("Покупки", "Молоко, хлеб, яйца", "еда,дом", 1),
        ("Работа", "Сделать проект по Flask", "работа,срочно", 1),
        ("Книги", "Прочитать 'Чистый код'", "развитие,книги", 2),
        ("Спорт", "Сходить в зал", "здоровье", 3)
    ]

    for title, content, tags, user_id in test_notes:
        cursor.execute(
            '''INSERT INTO note (title, content, tags, user_id, created_at, updated_at) 
               VALUES (?, ?, ?, ?, datetime('now'), datetime('now'))''',
            (title, content, tags, user_id)
        )
        print(f"   📝 Создана заметка: {title}")

    conn.commit()

    # Проверяем что добавилось
    cursor.execute("SELECT COUNT(*) FROM user")
    user_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM note")
    note_count = cursor.fetchone()[0]

    print(f"\n   ✅ Итого пользователей: {user_count}")
    print(f"   ✅ Итого заметок: {note_count}")

    conn.close()

    # 7. Финальная проверка
    print("\n" + "=" * 60)
    print("🎉 УСТАНОВКА ЗАВЕРШЕНА!")
    print("=" * 60)

    print("\n📋 ИТОГ:")
    print(f"   ✅ Зависимости установлены")
    print(f"   ✅ База данных создана: {db_path}")
    print(f"   ✅ Структура: 2 таблицы (user, note)")
    print(f"   ✅ Тестовые данные: 3 пользователя, 4 заметки")

    print("\n🚀 ЗАПУСК ПРИЛОЖЕНИЯ:")
    print("   1. Запустите приложение:")
    print("      python run.py --port 5001")
    print("   2. Откройте в браузере:")
    print("      http://localhost:5001")
    print("   3. Или если порт 5001 занят:")
    print("      http://localhost:5000")

    print("\n🔑 ТЕСТОВЫЕ АККАУНТЫ (пароли как есть):")
    print("   👤 alex / 123")
    print("   👤 masha / 456")
    print("   👤 ivan / 789")

    print("\n📂 СТРУКТУРА ПРОЕКТА:")
    print("   instance/notes.db      - база данных SQLite")
    print("   templates/             - шаблоны HTML")
    print("   templates/notes/       - шаблоны заметок")
    print("   templates/auth/        - шаблоны аутентификации")
    print("   app/__init__.py        - инициализация Flask")
    print("   app/models.py          - модели User и Note")
    print("   app/routes.py          - маршруты приложения")
    print("   app/forms.py           - формы WTForms")

    print("\n" + "=" * 60)
    print("⚠️  ВАЖНО: Если Flask не запускается из-за порта,")
    print("   используйте другой порт: python run.py --port 8080")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Установка прервана пользователем")
    except Exception as e:
        print(f"\n\n❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        print("\n🔧 Ручная установка:")
        print("   1. pip install flask flask-sqlalchemy flask-login flask-wtf")
        print("   2. python run.py --port 5001")