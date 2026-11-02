# Bank Statement Analyser – System Architecture

## 1. Overview

The application uses Python to process PDF bank statements, PostgreSQL to store transactions, and Streamlit to display financial reports.

## 2. Data Processing Workflow

```text
PDF Bank Statement
        ↓
PyMuPDF – Extract Transactions
        ↓
Pandas – Clean and Validate Data
        ↓
Python – Categorise Transactions
        ↓
PostgreSQL – Store Transactions
        ↓
SQL – Analyse Financial Data
        ↓
Streamlit and Plotly – Display Dashboard
```

## 3. Project Structure

| File | Purpose |
|---|---|
| `statement_reader.py` | Extracts transactions from PDF statements |
| `processor.py` | Cleans and validates data |
| `categoriser.py` | Assigns transaction categories |
| `database.py` | Connects to PostgreSQL and saves transactions |
| `analysis.py` | Runs SQL queries for financial analysis |
| `main.py` | Manages the PDF import process |
| `app.py` | Displays the interactive dashboard |

## 4. Design Decisions

- **Python:** Used for data processing and automation.
- **Pandas:** Used for cleaning and organising financial data.
- **PostgreSQL:** Stores transactions for long-term analysis.
- **SQL:** Calculates financial totals and filters transactions.
- **Streamlit:** Provides an interactive dashboard without requiring a separate frontend application.
- **Plotly:** Creates interactive financial charts.

## 5. Future Improvements

- Upload PDF statements directly through Streamlit.
- Support statements from different banks.
- Improve transaction categorisation.
- Add monthly comparisons and financial trends.
- Introduce automated data quality checks.