from ingestion.csv_source import CSVSource
from ingestion.pipeline import IngestionPipeline
from ingestion.repository import FinanceRepository
import config
import pandas as pd

source = CSVSource("data/payments.csv")
df = source.read()

# Explicitly parse the payment_date
df["payment_date"] = pd.to_datetime(df["payment_date"])

class ParsedCSVSource(CSVSource):
    def read(self):
        return df

parsed_source = ParsedCSVSource("data/payments.csv")
repo = FinanceRepository(config)
pipeline = IngestionPipeline(parsed_source, repo, "payments")
pipeline.run()

print("Payments loaded")