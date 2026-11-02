import pandas as pd

from analysis import get_spending_by_category


def clean_data(df):
    df = df.copy()
    df["Date"] = pd.to_datetime(
        df["Date"],
        format="%d %b %y",
        errors="coerce"
    )

    money_columns = ["MoneyIn", "MoneyOut", "Balance"]

    for col in money_columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .str.replace(",", "", regex=False)
            .replace({"blank": "0", "": "0"})
        )

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    return df

def validate_data(df):
    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate transactions:")
    print(df.duplicated().sum())

    print("\nNegative amounts:")
    print((df[["MoneyIn", "MoneyOut"]] < 0).sum())

    invalid_transactions = df[
        (df["MoneyIn"] > 0) &
        (df["MoneyOut"] > 0)
        ]

    print("\nTransactions with both money in and out:")
    print(len(invalid_transactions))

    return df

def get_category_dataframe():

    results = get_spending_by_category()

    columns = [
        "Category",
        "TransactionCount",
        "TotalMoneyOut"
    ]

    df = pd.DataFrame(
        results,
        columns=columns
    )

    return df


