
import pymupdf
import re
import pandas as pd


class StatementReader:

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def read(self):
        text = ""

        with pymupdf.open(self.pdf_path) as pdf:
            for page in pdf:
                text += page.get_text() + "\n"

        return text


    def extract_transactions(self, text):

        pattern = (
            r"Date\n(\d{2} [A-Za-z]{3} \d{2})\.\n"
            r"Description\n([^\n]+)\.\n"
            r"Type\n([A-Z]+)\.\n"
            r"Money In \(£\)\n([\d,.-]+|blank)\.\n"
            r"Money Out \(£\)\n([\d,.-]+|blank)\.\n"
            r"Balance \(£\)\n(-?[\d,]+\.\d{2})\."
        )

        records = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        columns = [
            "Date",
            "Description",
            "Type",
            "MoneyIn",
            "MoneyOut",
            "Balance"
        ]

        df = pd.DataFrame(records, columns=columns)

        return df
