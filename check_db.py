# check_db.py
from app import create_app
from app.models import db

app = create_app()

with app.app_context():
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print('📊 Таблицы в базе:', tables)
    for table in tables:
        print(f'\n{table}:')
        for column in inspector.get_columns(table):
            print(f'  - {column["name"]}: {column["type"]}')