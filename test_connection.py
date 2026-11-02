
from database import DatabaseManager

db = DatabaseManager()

with db.connect() as connection:
    with connection.cursor() as cursor:

        cursor.execute("""
            SELECT
                current_database(),
                to_regclass('public.transactions')
        """)

        print(cursor.fetchone())
