from ingestion.csv_source import CSVSource
from ingestion.pipeline import IngestionPipeline
from ingestion.repository import FinanceRepository

import pandas as pd

# Load source CSV
source = CSVSource("data/invoices.csv")

# Force date parsing on the loaded DataFrame before writing
df = source.read()

# Explicitly parse dates for CI and Postgres type safety
df["issue_date"] = pd.to_datetime(df["issue_date"])
df["due_date"] = pd.to_datetime(df["due_date"])

# Replace the CSVSource with our parsed DataFrame
class ParsedCSVSource(CSVSource):
    def read(self):
        return df

parsed_source = ParsedCSVSource("data/invoices.csv")

# Repository
repo = FinanceRepository()

# Pipeline
pipeline = IngestionPipeline(parsed_source, repo, "invoices")
pipeline.run()

print("Invoices loaded")