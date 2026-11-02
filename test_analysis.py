import pandas as pd
from database import DatabaseManager
from analysis import get_spending_by_category

spending = get_spending_by_category()

for category, count, amount in spending:
    print(f"{category}: {count} transactions, £{amount:.2f}")


from analysis import get_category_dataframe

category_df = get_category_dataframe()

print("Object type:", type(category_df))

print(category_df.head())

print(category_df.dtypes)
