
import hashlib
from pathlib import Path

from statement_reader import StatementReader
from processor import clean_data, validate_data
from categoriser import add_categories
from database import DatabaseManager


# Step 1: Select PDF
pdf_path = Path("2024_August_Statement.pdf")

# Step 2: Read PDF
reader = StatementReader(pdf_path)
text = reader.read()

# Step 3: Extract transactions
df = reader.extract_transactions(text)

# Step 4: Clean data
df = clean_data(df)

# Step 5: Validate data
df = validate_data(df)

# Step 6: Categorise transactions
df = add_categories(df)

# Step 7: Generate unique statement ID
statement_id = hashlib.sha256(
    pdf_path.read_bytes()
).hexdigest()

# Step 8: Create database manager
db = DatabaseManager()

# Step 9: Insert all transactions
db.insert_transactions(df, statement_id)

print("\nBank statement import completed.")
print("Total extracted transactions:", len(df))
