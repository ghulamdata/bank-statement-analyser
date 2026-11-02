
import os
import psycopg
from dotenv import load_dotenv


class DatabaseManager:

    def __init__(self):
        load_dotenv()

        self.connection_string = os.getenv(
            "DATABASE_URL"
        )

    def connect(self):

        if not self.connection_string:
            raise ValueError(
                "DATABASE_URL is missing"
            )

        connection = psycopg.connect(
            self.connection_string
        )

        return connection



    def insert_transactions(self, df, statement_id):

        query = """
            INSERT INTO transactions (
                transaction_date,
                description,
                transaction_type,
                money_in,
                money_out,
                balance,
                category,
                statement_id,
                row_number
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (statement_id, row_number)
            DO NOTHING
        """

        with self.connect() as connection:
            with connection.cursor() as cursor:

                for row_number, row in enumerate(
                    df.itertuples(index=False),
                    start=1
                ):
                    cursor.execute(
                        query,
                        (
                            row.Date.date(),
                            row.Description,
                            row.Type,
                            row.MoneyIn,
                            row.MoneyOut,
                            row.Balance,
                            row.Category,
                            statement_id,
                            row_number
                        )
                    )
