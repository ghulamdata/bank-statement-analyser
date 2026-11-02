
import pandas as pd
from database import DatabaseManager


# 1. Get available months
def get_available_months():

    db = DatabaseManager()

    query = """
        SELECT DISTINCT
            TO_CHAR(transaction_date, 'YYYY-MM') AS month
        FROM public.transactions
        ORDER BY month DESC;
    """

    with db.connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

    return [row[0] for row in results]


# 2. Get earliest and latest transaction dates
def get_date_limits():

    db = DatabaseManager()

    query = """
        SELECT
            MIN(transaction_date),
            MAX(transaction_date)
        FROM public.transactions;
    """

    with db.connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchone()


# 3. Calculate income, money out and net cash flow
def get_financial_summary(start_date=None, end_date=None):

    db = DatabaseManager()

    query = """
        SELECT
            COALESCE(SUM(money_in), 0),
            COALESCE(SUM(money_out), 0),
            COALESCE(SUM(money_in), 0)
                - COALESCE(SUM(money_out), 0)
        FROM public.transactions
        WHERE
            (%s::date IS NULL OR transaction_date >= %s::date)
            AND
            (%s::date IS NULL OR transaction_date <= %s::date);
    """

    params = (
        start_date, start_date,
        end_date, end_date
    )

    with db.connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()


# 4. Calculate money out by category
def get_spending_by_category(start_date=None, end_date=None):

    db = DatabaseManager()

    query = """
        SELECT
            category,
            COUNT(*) AS transaction_count,
            COALESCE(SUM(money_out), 0) AS total_money_out
        FROM public.transactions
        WHERE
            (%s::date IS NULL OR transaction_date >= %s::date)
            AND
            (%s::date IS NULL OR transaction_date <= %s::date)
        GROUP BY category
        ORDER BY total_money_out DESC;
    """

    params = (
        start_date, start_date,
        end_date, end_date
    )

    with db.connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()


# 5. Convert category results into a Pandas DataFrame
def get_category_dataframe(start_date=None, end_date=None):

    results = get_spending_by_category(
        start_date,
        end_date
    )

    df = pd.DataFrame(
        results,
        columns=[
            "Category",
            "TransactionCount",
            "TotalMoneyOut"
        ]
    )

    df["TotalMoneyOut"] = pd.to_numeric(
        df["TotalMoneyOut"]
    )

    return df
